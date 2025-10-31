"""
LangFlow Sync Agent - Exporta flows do LangFlow como JSON
"""
import requests
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime

LANGFLOW_URL = "http://langflow:7860"
OUTPUT_DIR = Path("/app/langflow-flows")
SYNC_INTERVAL = 60  # segundos

def get_file_hash(content: str) -> str:
    """Calcula hash SHA256 do conteúdo"""
    return hashlib.sha256(content.encode()).hexdigest()

def export_flows():
    """Exporta todos os flows do LangFlow como JSON"""
    try:
        # Lista flows
        response = requests.get(f"{LANGFLOW_URL}/api/v1/flows", timeout=10)
        response.raise_for_status()
        flows = response.json()
        
        if not flows:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Nenhum flow encontrado")
            return
        
        for flow in flows:
            flow_id = flow.get("id")
            flow_name = flow.get("name", "unnamed")
            
            # Converte nome para snake_case
            safe_name = flow_name.lower().replace(" ", "_").replace("-", "_")
            safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
            
            # Exporta JSON do flow
            flow_response = requests.get(
                f"{LANGFLOW_URL}/api/v1/flows/{flow_id}",
                timeout=10
            )
            flow_response.raise_for_status()
            flow_json = flow_response.json()
            
            # Serializa JSON
            json_content = json.dumps(flow_json, indent=2, ensure_ascii=False)
            
            # Verifica se mudou
            output_path = OUTPUT_DIR / f"{safe_name}.json"
            
            if output_path.exists():
                existing_content = output_path.read_text(encoding="utf-8")
                if get_file_hash(existing_content) == get_file_hash(json_content):
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏭️  {safe_name}.json (sem mudanças)")
                    continue
            
            # Salva
            output_path.write_text(json_content, encoding="utf-8")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ {safe_name}.json (exportado)")
            
    except requests.exceptions.ConnectionError:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ LangFlow não está acessível em {LANGFLOW_URL}")
    except requests.exceptions.Timeout:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏱️  Timeout ao conectar no LangFlow")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Erro: {e}")

def main():
    """Loop principal"""
    print("🚀 LangFlow Sync Agent iniciado")
    print(f"📡 LangFlow URL: {LANGFLOW_URL}")
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"⏱️  Intervalo: {SYNC_INTERVAL}s\n")
    
    # Cria diretório se não existir
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    while True:
        export_flows()
        time.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    main()
