# 🔧 JUSCRASH - Sync Tradutor

Tradução automática de workflows LangFlow (JSON) para LangGraph (Python) usando Claude 4.5 Sonnet.

---

## 🎯 Visão Geral

```mermaid
graph LR
    FS[(💾 workflow.json)]:::fs --> ST[🔧 Sync Tradutor]:::tradutor
    ST -->|Invoca| AI[🧠 Claude 4.5<br/>Sonnet]:::ai
    AI -->|Gera| PY[📄 workflow.py]:::py
    ST -->|Valida| PY
    ST -->|Atualiza| BE[⚙️ Backend]:::backend
    
    classDef fs fill:#8B5CF6,stroke:#6D28D9,stroke-width:2px,color:#fff
    classDef tradutor fill:#EC4899,stroke:#BE185D,stroke-width:3px,color:#fff
    classDef ai fill:#FF9900,stroke:#CC7A00,stroke-width:3px,color:#fff
    classDef py fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef backend fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```

**Função:** Traduz automaticamente `workflow.json` → `workflow.py` usando IA

**Modelo:** `us.anthropic.claude-sonnet-4-5-20250929-v1:0` (Bedrock Inference Profile)

---

## 🔄 Fluxo de Tradução

```mermaid
sequenceDiagram
    participant F as 💾 workflow.json
    participant S as 🔧 Sync Tradutor
    participant A as 🧠 Claude 4.5
    participant B as ⚙️ Backend
    participant H as 🏥 Health Check

    rect rgb(236, 72, 153, 0.1)
        Note over F,S: 1. Detecção (10s interval)
        S->>F: Monitora updated_at
        F-->>S: Detecta mudança
    end
    
    rect rgb(255, 153, 0, 0.1)
        Note over S,A: 2. Tradução via IA
        S->>S: Extrai nós relevantes (reduz 90%)
        S->>A: Prompt + workflow.json
        A->>A: Traduz JSON → Python
        A-->>S: workflow.py gerado
    end
    
    rect rgb(59, 130, 246, 0.1)
        Note over S,B: 3. Validação
        S->>S: Valida sintaxe Python
        S->>S: Verifica imports obrigatórios
        S->>B: Substitui workflow.py (temp)
        S->>H: GET /health
        
        alt API responde OK
            H-->>S: 200 OK
            S->>B: Confirma atualização ✅
        else API falha
            H-->>S: Erro
            S->>S: Reverte para backup ❌
        end
    end
```

**Tempo médio:** ~30-40 segundos  
**Rate limit:** 30s entre requests Bedrock

---

## 🧠 Prompt Engineering

### Estratégia de Redução

```mermaid
graph LR
    Full[📄 workflow.json<br/>~50k chars]:::full --> Extract[🔍 Extração]:::process
    Extract --> Relevant[📋 Nós Relevantes<br/>~5k chars]:::reduced
    Relevant --> AI[🧠 Claude 4.5]:::ai
    
    classDef full fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    classDef process fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef reduced fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef ai fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
```

**Redução:** ~90% do tamanho original

**Campos extraídos:**
- Tipo do nó
- ID do nó
- Campos essenciais (sem `code`, `tools_metadata`)
- Conexões (edges)

### Prompt Template

```python
prompt = f"""Você é um tradutor de workflows LangFlow para LangGraph.

## 🎯 TAREFA
Reconstrua o arquivo workflow.py mantendo a estrutura do arquivo de referência, 
mas USANDO o system_prompt do Agent do LangFlow.

## 📋 NÓS RELEVANTES DO LANGFLOW
```json
{relevant_nodes}
```

## 📚 ARQUIVOS DE REFERÊNCIA
- workflow.py ATUAL (MANTENHA ESTA ESTRUTURA)
- models.py (schemas Pydantic - NÃO MODIFIQUE)
- llm_service.py (USE o llm daqui - NÃO CRIE NOVO)

## ⚠️ REGRAS CRÍTICAS
1. PRESERVE a estrutura EXATA do workflow.py atual
2. USE o campo 'system_prompt' do nó Agent do LangFlow
3. Use 'from app.llm_service import llm'
4. Use 'from app.models import Processo, DecisionResponse'
5. Mantenha: WorkflowState, prompt, chain, analyze_node, create_workflow
6. Retorne APENAS o código Python completo

Gere o workflow.py:
"""
```

---

## ✅ Validação em 3 Camadas

### 1. Sintaxe Python

```python
def validate_python_syntax(code: str) -> tuple[bool, list[str]]:
    try:
        compile(code, '<string>', 'exec')
        ast.parse(code)
        return True, []
    except SyntaxError as e:
        return False, [f"Erro linha {e.lineno}: {e.msg}"]
```

### 2. Imports Obrigatórios

```python
required = [
    'from langgraph.graph',
    'from app.models',
    'from app.llm_service'
]
```

### 3. Health Check API

```python
# Substitui workflow.py temporariamente
# Testa GET /health
# Se OK: confirma
# Se erro: reverte
```

---

## 📦 Estrutura de Arquivos

```
app-local/
├── langflow-flows/
│   ├── workflow.json          # Input (gerado pelo Sync Agent)
│   └── .workflow_hash         # Tracking de mudanças
├── backend/app/
│   ├── workflow.py            # Output (gerado pelo Tradutor)
│   ├── workflow.py.bak.*      # Backups automáticos
│   ├── workflow.py.failed.*   # Tentativas falhadas (debug)
│   ├── models.py              # Referência (não modifica)
│   └── llm_service.py         # Referência (não modifica)
└── sync-agent/
    └── sync_tradutor.py       # Código do tradutor
```

---

## 🔧 Configuração

### Variáveis de Ambiente

**Arquivo:** `keys/.env`

```bash
# AWS Bedrock
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0
```

### Docker Compose

```yaml
sync-tradutor:
  build: ./sync-agent
  volumes:
    - ./langflow-flows:/app/langflow-flows
    - ./backend/app:/app/backend/app
  env_file:
    - ../keys/.env
  networks:
    - juscrash-network
  depends_on:
    - sync-agent
    - backend
  command: ["python", "-u", "sync_tradutor.py"]
```

---

## 📊 Logs

```bash
# Ver logs do Sync Tradutor
docker logs -f juscrash-sync-tradutor

# Exemplo de saída
🔄 SYNC TRADUTOR - 2025-01-20 10:30:00
[10:30:00] 💾 Flow salvo (2025-01-20T10:29:55) - Iniciando tradução...
[10:30:00] 🔄 Iniciando tradução...
[10:30:00] 📥 Arquivos lidos:
  - workflow.json: 45000 chars
  - 8 nós, 7 conexões
[10:30:05] 🤖 Invocando Bedrock Converse API...
[10:30:35] ✅ Resposta recebida (3500 chars)
[10:30:35] 📊 Tokens: 8500 input / 1200 output
[10:30:35] 🧪 Iniciando validação...
[10:30:35] ✅ Sintaxe válida
[10:30:37] 🧪 Testando workflow via API...
[10:30:39] ✅ API respondeu OK
[10:30:39] 💾 Criando backup...
[10:30:39] ✅ workflow.py atualizado
[10:30:39] ✅ TRADUÇÃO CONCLUÍDA COM SUCESSO!
```

---

## 💰 Custos

**Claude 4.5 Sonnet (Bedrock):**
- Input: ~8.500 tokens × $0.003/1k = $0.0255
- Output: ~1.200 tokens × $0.015/1k = $0.018
- **Total por tradução:** ~$0.04

**Frequência:** Apenas quando workflow.json é modificado

---

## 🐛 Troubleshooting

| Problema | Solução |
|----------|---------|
| ThrottlingException | Rate limit de 30s entre requests (automático) |
| Sintaxe inválida | Código salvo em `workflow.py.failed.*` para debug |
| API não responde | Reverte para backup automaticamente |
| Bedrock não conecta | Verificar credenciais AWS em `keys/.env` |

### Debug de Falhas

```bash
# Ver tentativas falhadas
ls -la app-local/backend/app/workflow.py.failed.*

# Ver backups
ls -la app-local/backend/app/workflow.py.bak.*

# Restaurar backup manualmente
cp app-local/backend/app/workflow.py.bak.1234567890 \
   app-local/backend/app/workflow.py
```

---

## 🔄 Workflow Completo (Sync Agent + Tradutor)

```mermaid
graph TB
    Dev[👨💻 Dev]:::dev --> LF[🎨 LangFlow]:::langflow
    LF --> PG[(🗄️ PostgreSQL)]:::db
    
    SA[🔄 Sync Agent]:::sync
    PG <--> SA
    SA <--> FS[(💾 workflow.json)]:::fs
    
    ST[🔧 Sync Tradutor]:::tradutor
    FS --> ST
    ST --> AI[🧠 Claude 4.5]:::ai
    ST --> BE[⚙️ Backend]:::backend
    
    classDef dev fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef langflow fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef db fill:#6366F1,stroke:#4338CA,stroke-width:2px,color:#fff
    classDef sync fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef fs fill:#8B5CF6,stroke:#6D28D9,stroke-width:2px,color:#fff
    classDef tradutor fill:#EC4899,stroke:#BE185D,stroke-width:3px,color:#fff
    classDef ai fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef backend fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```

**Fluxo:**
1. Dev edita no LangFlow
2. Sync Agent exporta para JSON
3. Sync Tradutor detecta mudança
4. Claude 4.5 traduz JSON → Python
5. Backend atualizado automaticamente

---

## 📚 Referências

- [SYNC_FLOW.md](SYNC_FLOW.md) - Sync Agent (LangFlow ⇄ JSON)
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura completa
- Código: `app-local/sync-agent/sync_tradutor.py`

---

**Autor:** José Cleiton  
**Projeto:** JUSCASH  
**Versão:** 1.0
