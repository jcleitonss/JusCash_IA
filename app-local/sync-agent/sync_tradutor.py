"""
Sync Tradutor - LangFlow JSON → LangGraph Python
Usa Bedrock Converse API para tradução com Claude 4.5
"""

import os
import json
import time
import hashlib
import ast
import boto3
from pathlib import Path
from datetime import datetime
import psycopg2

# ============ RATE LIMITING ============
LAST_REQUEST_TIME = 0
RATE_LIMIT_SECONDS = 30

# ============ CONFIGURAÇÃO ============
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")

# Caminhos
FLOW_JSON = Path("/app/langflow-flows/workflow.json")
WORKFLOW_PY = Path("/app/backend/app/workflow.py")
MODELS_PY = Path("/app/backend/app/models.py")
LLM_SERVICE_PY = Path("/app/backend/app/llm_service.py")
HASH_FILE = Path("/app/langflow-flows/.workflow_hash")

# Cliente Bedrock Runtime
bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

print(f"🤖 Sync Tradutor inicializado")
print(f"📍 Região: {AWS_REGION}")
print(f"🧠 Modelo: {BEDROCK_MODEL_ID}")

# ============ FUNÇÕES AUXILIARES ============
def get_file_hash(path: Path) -> str:
    """Calcula hash SHA256 do arquivo"""
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_text(encoding="utf-8").encode()).hexdigest()

def wait_rate_limit():
    """Aguarda rate limit de 30s entre requests"""
    global LAST_REQUEST_TIME
    
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < RATE_LIMIT_SECONDS:
        wait_time = RATE_LIMIT_SECONDS - elapsed
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] ⏳ Rate limit: aguardando {wait_time:.1f}s...")
        time.sleep(wait_time)
    
    LAST_REQUEST_TIME = time.time()

def invoke_bedrock(prompt: str, max_tokens: int = 4096, retry_count: int = 0) -> str:
    """Invoca Bedrock Converse API (suporta Inference Profiles)"""
    wait_rate_limit()
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] 🤖 Invocando Bedrock Converse API...")
    print(f"[{timestamp}] 🧠 Modelo: {BEDROCK_MODEL_ID}")
    
    try:
        response = bedrock_runtime.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=[{
                "role": "user",
                "content": [{"text": prompt}]
            }],
            inferenceConfig={
                "temperature": 0.1,
                "maxTokens": max_tokens
            }
        )
        
        text = response['output']['message']['content'][0]['text']
        tokens_in = response['usage']['inputTokens']
        tokens_out = response['usage']['outputTokens']
        
        print(f"[{timestamp}] ✅ Resposta recebida ({len(text)} chars)")
        print(f"[{timestamp}] 📊 Tokens: {tokens_in} input / {tokens_out} output")
        return text
        
    except Exception as e:
        error_msg = str(e)
        
        if "ThrottlingException" in error_msg or "Too many requests" in error_msg:
            if retry_count < 5:
                wait_time = (2 ** retry_count) * 10
                print(f"[{timestamp}] ⚠️  Throttling - Retry {retry_count + 1}/5 em {wait_time}s")
                time.sleep(wait_time)
                return invoke_bedrock(prompt, max_tokens, retry_count + 1)
        
        print(f"[{timestamp}] ❌ Erro: {e}")
        raise

def validate_python_syntax(code: str) -> tuple[bool, list[str]]:
    """Valida sintaxe Python localmente"""
    errors = []
    
    try:
        compile(code, '<string>', 'exec')
        ast.parse(code)
    except SyntaxError as e:
        errors.append(f"Erro de sintaxe linha {e.lineno}: {e.msg}")
        return False, errors
    except Exception as e:
        errors.append(f"Erro ao validar: {str(e)}")
        return False, errors
    
    required = ['from langgraph.graph', 'from app.models', 'from app.llm_service']
    for req in required:
        if req not in code:
            errors.append(f"Import obrigatório faltando: {req}")
    
    if 'def create_workflow()' not in code:
        errors.append("Função create_workflow() não encontrada")
    
    if errors:
        return False, errors
    
    return True, []

# ============ EXTRAÇÃO DE NÓS RELEVANTES ============
def extract_relevant_nodes(flow_data: dict) -> dict:
    """Extrai APENAS dados essenciais (reduz ~90% do tamanho)"""
    nodes = flow_data.get('data', {}).get('nodes', [])
    edges = flow_data.get('data', {}).get('edges', [])
    
    relevant_nodes = []
    
    for node in nodes:
        node_type = node.get('data', {}).get('type', '')
        node_id = node.get('id', '')
        
        if node_type in ['note', 'noteNode']:
            continue
        
        template = node.get('data', {}).get('node', {}).get('template', {})
        
        essential_fields = {}
        for key, value in template.items():
            if key in ['code', 'tools_metadata', '_type']:
                continue
            
            if isinstance(value, dict):
                field_value = value.get('value')
                if field_value and field_value != '__UNDEFINED__' and field_value != '':
                    essential_fields[key] = field_value
            elif value:
                essential_fields[key] = value
        
        relevant_nodes.append({
            'id': node_id,
            'type': node_type,
            'fields': essential_fields
        })
    
    simple_edges = [
        {'from': e.get('source'), 'to': e.get('target')}
        for e in edges
    ]
    
    return {
        'nodes': relevant_nodes,
        'edges': simple_edges,
        'summary': f"{len(relevant_nodes)} nós, {len(simple_edges)} conexões"
    }

# ============ TRADUÇÃO ============
def translate_workflow() -> str:
    """Traduz workflow.json → workflow.py"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{timestamp}] 🔄 Iniciando tradução...")
    
    flow_json_raw = FLOW_JSON.read_text(encoding="utf-8")
    flow_data = json.loads(flow_json_raw)
    models_py = MODELS_PY.read_text(encoding="utf-8")
    llm_service_py = LLM_SERVICE_PY.read_text(encoding="utf-8")
    workflow_atual = WORKFLOW_PY.read_text(encoding="utf-8")
    
    relevant = extract_relevant_nodes(flow_data)
    
    print(f"[{timestamp}] 📥 Arquivos lidos:")
    print(f"  - workflow.json: {len(flow_json_raw)} chars")
    print(f"  - {relevant['summary']}")
    print(f"  - models.py: {len(models_py)} chars")
    print(f"  - llm_service.py: {len(llm_service_py)} chars")
    print(f"  - workflow.py atual: {len(workflow_atual)} chars")
    
    full_prompt = f"""Você é um tradutor de workflows LangFlow para LangGraph.

## 🎯 TAREFA
Reconstrua o arquivo workflow.py mantendo a estrutura do arquivo de referência, mas USANDO o system_prompt do Agent do LangFlow.

## 📋 NÓS RELEVANTES DO LANGFLOW
```json
{json.dumps(relevant, indent=2, ensure_ascii=False)}
```

## 📚 ARQUIVOS DE REFERÊNCIA

### workflow.py ATUAL (MANTENHA ESTA ESTRUTURA)
```python
{workflow_atual}
```

### models.py (schemas Pydantic - NÃO MODIFIQUE)
```python
{models_py}
```

### llm_service.py (USE o llm daqui - NÃO CRIE NOVO)
```python
{llm_service_py}
```

## ⚠️ REGRAS CRÍTICAS
1. PRESERVE a estrutura EXATA do workflow.py atual
2. USE o campo 'system_prompt' do nó Agent do LangFlow no ChatPromptTemplate
3. Use 'from app.llm_service import llm' (NÃO crie novo cliente Bedrock)
4. Use 'from app.models import Processo, DecisionResponse'
5. Mantenha: WorkflowState, prompt, chain, analyze_node, create_workflow, app_workflow
6. NÃO invente schemas novos
7. Retorne APENAS o código Python completo, sem explicações

Gere o workflow.py:
"""
    
    response = invoke_bedrock(full_prompt, max_tokens=2048)
    
    code_start = response.find("```python")
    code_end = response.rfind("```")
    
    if code_start >= 0 and code_end > code_start:
        code = response[code_start + 9:code_end].strip()
        print(f"[{timestamp}] ✅ Código extraído ({len(code)} chars)")
        return code
    else:
        print(f"[{timestamp}] ⚠️  Código não encontrado em blocos markdown, usando resposta completa")
        return response.strip()

# ============ VALIDAÇÃO ============
def test_code_via_api(code: str) -> tuple[bool, list[str]]:
    """Valida testando na própria API do backend"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] 🧪 Testando workflow via API...")
    
    temp_path = WORKFLOW_PY.with_suffix('.py.temp')
    temp_path.write_text(code, encoding='utf-8')
    
    backup = WORKFLOW_PY.read_text(encoding='utf-8')
    WORKFLOW_PY.write_text(code, encoding='utf-8')
    
    try:
        time.sleep(2)
        
        import requests
        response = requests.get('http://juscrash-backend:8000/health', timeout=5)
        
        if response.status_code == 200:
            print(f"[{timestamp}] ✅ API respondeu OK")
            return True, []
        else:
            error = f"API retornou status {response.status_code}"
            print(f"[{timestamp}] ❌ {error}")
            return False, [error]
            
    except Exception as e:
        error = f"Erro ao testar API: {str(e)}"
        print(f"[{timestamp}] ❌ {error}")
        return False, [error]
        
    finally:
        WORKFLOW_PY.write_text(backup, encoding='utf-8')
        if temp_path.exists():
            temp_path.unlink()

def test_code(code: str) -> tuple[bool, list[str]]:
    """Valida código Python"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{timestamp}] 🧪 Iniciando validação...")
    
    print(f"[{timestamp}] 🔍 Validando sintaxe Python...")
    valid_syntax, syntax_errors = validate_python_syntax(code)
    
    if not valid_syntax:
        print(f"[{timestamp}] ❌ Erros de sintaxe:")
        for error in syntax_errors:
            print(f"     - {error}")
        return False, syntax_errors
    
    print(f"[{timestamp}] ✅ Sintaxe válida")
    
    return test_code_via_api(code)

# ============ DEPLOY ============
def backup_and_replace(code: str):
    """Cria backup e substitui workflow.py"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{timestamp}] 💾 Criando backup...")
    
    backup_path = WORKFLOW_PY.with_suffix(f".py.bak.{int(datetime.now().timestamp())}")
    backup_path.write_text(WORKFLOW_PY.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"[{timestamp}] ✅ Backup criado: {backup_path.name}")
    
    WORKFLOW_PY.write_text(code, encoding="utf-8")
    print(f"[{timestamp}] ✅ workflow.py atualizado")
    
    new_hash = get_file_hash(FLOW_JSON)
    HASH_FILE.write_text(new_hash)
    print(f"[{timestamp}] ✅ Hash atualizado")

def save_failed_attempt(code: str, errors: list[str]):
    """Salva tentativa falhada para debug"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    failed_path = WORKFLOW_PY.with_suffix(f".py.failed.{int(datetime.now().timestamp())}")
    
    content = f"""# TRADUÇÃO FALHADA - {datetime.now().isoformat()}
# ERROS:
{chr(10).join(f'# - {e}' for e in errors)}

{code}
"""
    
    failed_path.write_text(content, encoding="utf-8")
    print(f"[{timestamp}] 💾 Tentativa falhada salva: {failed_path.name}")

# ============ ORQUESTRAÇÃO ============
def sync_tradutor():
    """Fluxo completo: traduz → testa → deploy"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    print(f"\n{'='*60}")
    print(f"🔄 SYNC TRADUTOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    try:
        novo_codigo = translate_workflow()
        
        valid, errors = test_code(novo_codigo)
        
        if not valid:
            print(f"\n[{timestamp}] ❌ Código gerado é inválido")
            save_failed_attempt(novo_codigo, errors)
            return False
        
        backup_and_replace(novo_codigo)
        
        print(f"\n[{timestamp}] ✅ TRADUÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"{'='*60}\n")
        return True
        
    except Exception as e:
        print(f"\n[{timestamp}] ❌ Erro durante tradução: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============ WATCH LOOP ============
def watch_changes():
    """Monitora mudanças via updated_at do JSON (salvo pelo sync_bidirectional)"""
    print(f"\n🔄 Sync Tradutor iniciado - Monitorando salvamentos...")
    print(f"📁 Arquivo: {FLOW_JSON}")
    print(f"⏱️  Intervalo: 10s\n")
    
    last_updated = None
    
    while True:
        try:
            if not FLOW_JSON.exists():
                time.sleep(10)
                continue
            
            flow_data = json.loads(FLOW_JSON.read_text(encoding="utf-8"))
            current_updated = flow_data.get('updated_at')
            
            if current_updated and current_updated != last_updated:
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                if last_updated:
                    print(f"[{timestamp}] 💾 Flow salvo ({current_updated}) - Iniciando tradução...")
                    
                    if sync_tradutor():
                        last_updated = current_updated
                    else:
                        print(f"[{timestamp}] ⚠️  Tradução falhou - Mantendo workflow.py original")
                else:
                    print(f"[{timestamp}] 📖 Estado inicial carregado ({current_updated})")
                    last_updated = current_updated
            
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n👋 Sync Tradutor finalizado")
            break
        except json.JSONDecodeError:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] ⚠️  JSON inválido, aguardando...")
            time.sleep(10)
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] ❌ Erro no loop: {e}")
            time.sleep(10)

# ============ MAIN ============
if __name__ == "__main__":
    watch_changes()
