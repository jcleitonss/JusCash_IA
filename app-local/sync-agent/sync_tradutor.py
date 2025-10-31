"""
⚠️ SYNC TRADUTOR - INOPERANTE / DESABILITADO

Status: NÃO FUNCIONAL - EM DESENVOLVIMENTO
Motivo: Funcionalidade futura, ainda não implementada completamente
Uso: Não usar em produção

Quando funcionar:
- Sync Tradutor Minimalista - LangGraph ↔ LangFlow
- Foco: Extrair apenas nós essenciais (prompt, model, parser)
"""

# TODO: Implementar funcionalidade completa
# TODO: Testar conversão bidirecional
# TODO: Validar compatibilidade com LangFlow atual

import sys
print("⚠️  SYNC TRADUTOR DESABILITADO - Funcionalidade em desenvolvimento")
sys.exit(0)

# ============================================================================
# CÓDIGO COMENTADO - NÃO FUNCIONAL
# ============================================================================
"""
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime

FLOWS_DIR = Path("/app/langflow-flows")
BACKEND_DIR = Path("/app/backend/app")
WORKFLOW_FILE = BACKEND_DIR / "workflow.py"
PRINCIPAL_FLOW = FLOWS_DIR / "principal.json"
HASH_FILE = FLOWS_DIR / ".principal_hash"


def get_file_hash(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_text(encoding="utf-8").encode()).hexdigest()


def extract_system_prompt(code: str) -> str:
    match = re.search(r'\("system",\s*"""([^"]+)"""\)', code, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "Você é um analista jurídico especializado."


def extract_nodes_from_langflow(flow_data: dict) -> dict:
    nodes = {}
    
    for node in flow_data.get("nodes", []):
        node_type = node.get("data", {}).get("type")
        node_data = node.get("data", {}).get("node", {})
        
        if node_type in ["note", "noteNode"]:
            continue
        
        if "Prompt" in str(node_type) or "prompt" in str(node_type).lower():
            template = node_data.get("template", {})
            nodes["prompt"] = template.get("template", {}).get("value", "")
        
        elif "Bedrock" in str(node_type) or "bedrock" in str(node_type).lower():
            template = node_data.get("template", {})
            nodes["model_id"] = template.get("model_id", {}).get("value", "")
            nodes["temperature"] = template.get("temperature", {}).get("value", 0)
        
        elif "Parser" in str(node_type) or "parser" in str(node_type).lower():
            nodes["parser"] = "JsonOutputParser"
    
    return nodes


def langgraph_to_langflow():
    
    if not WORKFLOW_FILE.exists():
        print("⚠️  workflow.py não encontrado")
        return
    
    code = WORKFLOW_FILE.read_text(encoding="utf-8")
    system_prompt = extract_system_prompt(code)
    
    flow = {
        "nodes": [
            {
                "id": "ChatInput-1",
                "type": "genericNode",
                "position": {"x": 100, "y": 300},
                "data": {
                    "type": "ChatInput",
                    "node": {"display_name": "Input", "template": {}}
                }
            },
            {
                "id": "Prompt-1",
                "type": "genericNode",
                "position": {"x": 500, "y": 300},
                "data": {
                    "type": "PromptComponent",
                    "node": {
                        "display_name": "System Prompt",
                        "template": {
                            "template": {"value": system_prompt}
                        }
                    }
                }
            },
            {
                "id": "Bedrock-1",
                "type": "genericNode",
                "position": {"x": 900, "y": 300},
                "data": {
                    "type": "ChatBedrock",
                    "node": {
                        "display_name": "Bedrock Claude",
                        "template": {
                            "model_id": {"value": "anthropic.claude-3-5-sonnet-20240620-v1:0"},
                            "temperature": {"value": 0}
                        }
                    }
                }
            },
            {
                "id": "ChatOutput-1",
                "type": "genericNode",
                "position": {"x": 1300, "y": 300},
                "data": {
                    "type": "ChatOutput",
                    "node": {"display_name": "Output", "template": {}}
                }
            }
        ],
        "edges": [
            {"source": "ChatInput-1", "target": "Prompt-1"},
            {"source": "Prompt-1", "target": "Bedrock-1"},
            {"source": "Bedrock-1", "target": "ChatOutput-1"}
        ],
        "viewport": {"x": 0, "y": 0, "zoom": 1}
    }
    
    PRINCIPAL_FLOW.write_text(json.dumps(flow, indent=2), encoding="utf-8")
    HASH_FILE.write_text(get_file_hash(PRINCIPAL_FLOW))
    print("✅ principal.json criado")


def langflow_to_langgraph():
    
    if not PRINCIPAL_FLOW.exists():
        print("⚠️  principal.json não encontrado")
        return
    
    flow_data = json.loads(PRINCIPAL_FLOW.read_text(encoding="utf-8"))
    nodes = extract_nodes_from_langflow(flow_data)
    
    if not nodes.get("prompt"):
        print("⚠️  Nenhum prompt encontrado no flow")
        return
    
    if WORKFLOW_FILE.exists():
        backup = WORKFLOW_FILE.with_suffix(".py.bak")
        backup.write_text(WORKFLOW_FILE.read_text(encoding="utf-8"))
    
    code = WORKFLOW_FILE.read_text(encoding="utf-8")
    
    new_prompt = nodes["prompt"]
    pattern = r'(\("system",\s*""")([^"]+)("""\))'
    new_code = re.sub(pattern, rf'\1{new_prompt}\3', code, flags=re.DOTALL)
    
    if new_code != code:
        WORKFLOW_FILE.write_text(new_code, encoding="utf-8")
        HASH_FILE.write_text(get_file_hash(PRINCIPAL_FLOW))
        print("✅ workflow.py atualizado (prompt)")
    else:
        print("ℹ️  Nenhuma mudança detectada")


def watch_principal():
    import time
    
    print("🔄 Sync Tradutor iniciado")
    
    FLOWS_DIR.mkdir(parents=True, exist_ok=True)
    
    if not PRINCIPAL_FLOW.exists() and WORKFLOW_FILE.exists():
        print("🆕 Convertendo workflow.py → principal.json")
        langgraph_to_langflow()
    
    last_hash = get_file_hash(PRINCIPAL_FLOW)
    
    while True:
        current_hash = get_file_hash(PRINCIPAL_FLOW)
        
        if current_hash and current_hash != last_hash:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 principal.json alterado")
            langflow_to_langgraph()
            last_hash = current_hash
        
        time.sleep(10)


if __name__ == "__main__":
    watch_principal()
"""
