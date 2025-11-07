"""
Sync Bidirecional com Sentinela - LangFlow ↔ JSON
"""
import psycopg2
import json
import time
import hashlib
import os
import requests
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://langflow:langflow@postgres:5432/langflow")
FLOWS_DIR = Path("/app/langflow-flows")
COMPONENTS_DIR = FLOWS_DIR / "components"
MAPPING_FILE = FLOWS_DIR / "id_mapping.json"
INITIALIZED_FILE = FLOWS_DIR / ".initialized"
SYNC_INTERVAL = 60


def get_file_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


def get_db_connection():
    return psycopg2.connect(POSTGRES_URL)


def load_id_mapping():
    if MAPPING_FILE.exists():
        return json.loads(MAPPING_FILE.read_text(encoding="utf-8"))
    return {}


def save_id_mapping(mapping):
    MAPPING_FILE.write_text(json.dumps(mapping, indent=2), encoding="utf-8")


def safe_filename(name: str) -> str:
    safe_name = name.lower().replace(" ", "_").replace("-", "_")
    return "".join(c for c in safe_name if c.isalnum() or c == "_")


def get_db_flow_ids():
    """Retorna set de IDs dos flows no banco"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM flow WHERE user_id IS NOT NULL")
        ids = {row[0] for row in cursor.fetchall()}
        cursor.close()
        conn.close()
        return ids
    except:
        return set()


def export_flows():
    """Exporta flows do PostgreSQL para JSON com tracking por ID e timestamp"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, data, is_component, webhook, mcp_enabled, locked, description, updated_at 
            FROM flow WHERE user_id IS NOT NULL
        """)
        flows = cursor.fetchall()
        
        if not flows:
            cursor.close()
            conn.close()
            return
        
        id_mapping = load_id_mapping()
        current_ids = {row[0] for row in flows}
        
        # Detectar exclusões
        for flow_id, filename in list(id_mapping.items()):
            if flow_id not in current_ids:
                file_path = FLOWS_DIR / f"{filename}.json"
                if file_path.exists():
                    file_path.unlink()
                    print(f"🗑️  {filename}.json (excluído)")
                del id_mapping[flow_id]
        
        # Processar flows
        for flow_id, flow_name, flow_data, is_component, webhook, mcp_enabled, locked, description, updated_at in flows:
            new_filename = safe_filename(flow_name)
            old_filename = id_mapping.get(flow_id)
            
            # Criar objeto flow completo com metadados
            flow_complete = {
                "id": flow_id,
                "name": flow_name,
                "description": description,
                "data": flow_data,
                "is_component": is_component,
                "webhook": webhook,
                "mcp_enabled": mcp_enabled,
                "locked": locked,
                "updated_at": updated_at.isoformat() if updated_at else None
            }
            
            json_content = json.dumps(flow_complete, indent=2, ensure_ascii=False)
            output_path = FLOWS_DIR / f"{new_filename}.json"
            
            # Detectar renomeação
            if old_filename and old_filename != new_filename:
                old_path = FLOWS_DIR / f"{old_filename}.json"
                if old_path.exists():
                    old_path.rename(output_path)
                    print(f"📝 {old_filename}.json → {new_filename}.json")
            
            # Verificar se precisa atualizar (por timestamp ou hash)
            needs_update = True
            if output_path.exists():
                try:
                    existing_data = json.loads(output_path.read_text(encoding="utf-8"))
                    existing_updated = existing_data.get("updated_at")
                    
                    # Comparar por timestamp primeiro
                    if existing_updated and updated_at:
                        if existing_updated == flow_complete["updated_at"]:
                            needs_update = False
                    # Fallback: comparar hash
                    elif get_file_hash(json.dumps(existing_data)) == get_file_hash(json_content):
                        needs_update = False
                except:
                    needs_update = True
            
            if needs_update:
                output_path.write_text(json_content, encoding="utf-8")
                print(f"⬇️  {new_filename}.json (atualizado)")
            
            id_mapping[flow_id] = new_filename
        
        save_id_mapping(id_mapping)
        cursor.close()
        conn.close()
            
    except Exception as e:
        print(f"❌ Erro export: {e}")


def import_flows():
    """Importa apenas flows novos (que não existem no banco)"""
    json_files = [f for f in FLOWS_DIR.glob("*.json") if f.name not in ["id_mapping.json"]]
    if not json_files:
        return
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Pega IDs existentes no banco
        db_flow_ids = get_db_flow_ids()
        
        cursor.execute("SELECT id FROM \"user\" LIMIT 1")
        user_row = cursor.fetchone()
        if not user_row:
            cursor.close()
            conn.close()
            return
        
        user_id = user_row[0]
        
        for json_file in json_files:
            flow_data = json.loads(json_file.read_text(encoding="utf-8"))
            
            # Verifica se flow tem ID e se já existe no banco
            flow_id = flow_data.get("id")
            if flow_id and flow_id in db_flow_ids:
                continue
            
            flow_name = flow_data.get("name", json_file.stem)
            
            # Verifica por nome também
            cursor.execute("SELECT id FROM flow WHERE name = %s", (flow_name,))
            if cursor.fetchone():
                continue
            
            print(f"📝 Inserindo {json_file.name}")
            
            cursor.execute("""
                INSERT INTO flow (
                    id, name, data, user_id, 
                    is_component, webhook, mcp_enabled, locked,
                    access_type, updated_at
                ) 
                VALUES (gen_random_uuid(), %s, %s::jsonb, %s, %s::boolean, %s::boolean, %s::boolean, %s::boolean, %s, NOW())
            """, (flow_name, json.dumps(flow_data), user_id, False, False, True, False, 'PRIVATE'))
            
            conn.commit()
            
            # Busca ID do flow inserido e ativa na interface
            cursor.execute("SELECT id FROM flow WHERE name = %s", (flow_name,))
            new_flow = cursor.fetchone()
            if new_flow:
                flow_id = new_flow[0]
                url_internal = f"http://host.docker.internal:7860/flow/{flow_id}"
                url_localhost = f"http://localhost:7860/flow/{flow_id}"
                try:
                    print(f"🌐 Localhost: {url_localhost}")
                    print(f"🌐 Internal: {url_internal}")
                    with sync_playwright() as p:
                        browser = p.chromium.launch(headless=True)
                        page = browser.new_page()
                        page.goto(url_internal, wait_until="networkidle", timeout=30000)
                        time.sleep(5)
                        browser.close()
                    print(f"✅ {json_file.name} - Flow ativado")
                except Exception as e:
                    print(f"⬆️  {json_file.name} - Erro: {e}")
        
        cursor.close()
        conn.close()
                
    except Exception as e:
        print(f"❌ Erro import: {e}")


def extract_custom_components(flow_data: dict) -> dict:
    """Extrai componentes customizados do flow"""
    components = {}
    
    nodes = flow_data.get('data', {}).get('data', {}).get('nodes', [])
    
    for node in nodes:
        node_data = node.get('data', {})
        node_info = node_data.get('node', {})
        template = node_info.get('template', {})
        
        code_field = template.get('code', {})
        if isinstance(code_field, dict):
            code = code_field.get('value', '')
        else:
            code = code_field
            
        if code and len(code) > 100:
            component_type = node_data.get('type', 'Unknown')
            component_id = node.get('id', '')
            display_name = node_info.get('display_name', component_type)
            
            safe_name = safe_filename(display_name)
            
            components[component_id] = {
                'type': component_type,
                'display_name': display_name,
                'filename': f"{safe_name}.py",
                'code': code,
                'description': node_info.get('description', ''),
                'icon': node_info.get('icon', '')
            }
    
    return components


def sync_components():
    """Sincroniza componentes customizados dos flows"""
    COMPONENTS_DIR.mkdir(parents=True, exist_ok=True)
    
    for json_file in FLOWS_DIR.glob("*.json"):
        if json_file.name in ["id_mapping.json"]:
            continue
            
        try:
            flow_data = json.loads(json_file.read_text(encoding="utf-8"))
            components = extract_custom_components(flow_data)
            
            if components:
                print(f"🔍 {json_file.stem}: {len(components)} componente(s) customizado(s) detectado(s)")
                for comp_id, comp_info in components.items():
                    print(f"   └─ {comp_info['display_name']} ({comp_info['type']})")
                    
                    comp_file = COMPONENTS_DIR / comp_info['filename']
                    
                    header = f'''"""
Component: {comp_info['display_name']}
Type: {comp_info['type']}
Description: {comp_info['description']}
Icon: {comp_info['icon']}
Source Flow: {json_file.stem}
Component ID: {comp_id}
"""

'''
                    full_code = header + comp_info['code']
                    
                    if not comp_file.exists() or comp_file.read_text(encoding='utf-8') != full_code:
                        comp_file.write_text(full_code, encoding='utf-8')
                        print(f"      ✅ Salvo em components/{comp_info['filename']}")
            else:
                print(f"ℹ️  {json_file.stem}: Nenhum componente customizado")
                    
        except Exception as e:
            print(f"⚠️  Erro ao extrair componentes de {json_file.name}: {e}")


def wait_for_postgres():
    for i in range(30):
        try:
            conn = get_db_connection()
            conn.close()
            return True
        except:
            time.sleep(2)
    return False


def main():
    print("🔄 LangFlow Sync Bidirecional iniciado")
    
    FLOWS_DIR.mkdir(parents=True, exist_ok=True)
    
    if not wait_for_postgres():
        print("❌ PostgreSQL não disponível")
        return
    
    # Importa flows com sentinela
    if not INITIALIZED_FILE.exists():
        print("🆕 Primeira inicialização - importando flows...")
        import_flows()
        sync_components()
        INITIALIZED_FILE.write_text(f"Initialized at {datetime.now().isoformat()}")
        print("✅ Inicializado")
    else:
        print("♻️  Importando apenas novos flows...")
        import_flows()
        sync_components()
    
    # Loop bidirecional
    while True:
        export_flows()
        import_flows()
        sync_components()
        time.sleep(SYNC_INTERVAL)


if __name__ == "__main__":
    main()
