# 🔄 Sync Agent - LangFlow ↔ LangGraph

Sistema de sincronização bidirecional entre LangFlow (UI visual) e LangGraph (código Python).

## 🎯 Componentes

### 1. **sync_bidirectional.py**
Sincroniza flows entre LangFlow PostgreSQL e arquivos JSON.

**Funcionalidades:**
- ✅ Exporta flows do banco → JSON
- ✅ Importa JSONs novos → banco
- ✅ Detecta renomeações por ID
- ✅ Detecta exclusões
- ✅ Arquivo sentinela `.initialized`

### 2. **sync_tradutor.py**
Converte entre LangGraph (Python) e LangFlow (JSON) usando LLM.

**Funcionalidades:**
- ✅ Converte `workflow.py` → `principal.json`
- ✅ Converte `principal.json` → `workflow.py`
- ✅ Validação de sintaxe Python
- ✅ Backup automático (`.bak`)
- ✅ Usa Bedrock Claude para conversão

## 🚀 Como Usar

### Iniciar Serviços
```bash
cd app-local
docker-compose up -d sync-agent sync-tradutor
```

### Ver Logs
```bash
# Sync Agent (PostgreSQL ↔ JSON)
docker logs -f juscrash-sync-agent

# Sync Tradutor (LangGraph ↔ LangFlow)
docker logs -f juscrash-sync-tradutor
```

### ⚠️ Importar Workflow no LangFlow

**IMPORTANTE:** Para o workflow importado aparecer no LangFlow UI:

1. Rode o sync-agent e veja os logs:
```bash
docker logs -f juscrash-sync-agent
```

2. O log vai gerar um link como:
```
✅ Flow importado: principal
🔗 Abra no LangFlow: http://localhost:7860/flow/abc123-def456-...
```

3. **Clique no link** ou copie e cole no navegador
4. O workflow será carregado automaticamente no editor

> **Nota:** Apenas clicar no link uma vez é suficiente. Depois o flow fica salvo no LangFlow.

## 🔄 Fluxo Completo

### 1. Inicialização
```
workflow.py (LangGraph) → LLM → principal.json (LangFlow)
                                       ↓
                              Sync Agent → PostgreSQL
                                       ↓
                                  LangFlow UI
```

### 2. Edição no LangFlow UI
```
LangFlow UI → PostgreSQL → Sync Agent → principal.json
                                              ↓
                                    LLM → workflow.py (atualizado)
```

### 3. Edição no Código
```
workflow.py (editado) → LLM → principal.json
                                    ↓
                          Sync Agent → PostgreSQL
                                    ↓
                               LangFlow UI (atualizado)
```

## 📁 Estrutura de Arquivos

```
langflow-flows/
├── principal.json          # Flow principal (editável no LangFlow UI)
├── id_mapping.json         # Mapeamento ID → filename
├── .initialized            # Sentinela de inicialização
└── .principal_hash         # Hash para detectar mudanças

backend/app/
├── workflow.py             # LangGraph (código Python)
├── workflow.py.bak         # Backup automático
├── models.py               # Pydantic models
└── llm_service.py          # Configuração Bedrock
```

## ⚙️ Configuração

### Variáveis de Ambiente
```bash
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
POSTGRES_URL=postgresql://langflow:langflow@postgres:5432/langflow
```

## 🎯 Casos de Uso

### Desenvolver Visualmente
1. Edite flow "principal" no LangFlow UI (http://localhost:7860)
2. Sync tradutor detecta mudança
3. `workflow.py` é atualizado automaticamente

### Desenvolver em Código
1. Edite `backend/app/workflow.py`
2. Restart sync-tradutor
3. `principal.json` é atualizado
4. Flow aparece no LangFlow UI

### Adicionar Novo Flow
1. Adicione JSON em `langflow-flows/`
2. Restart sync-agent
3. Flow importado para PostgreSQL
4. **Clique no link gerado nos logs** para abrir no LangFlow UI

## 🔍 Troubleshooting

### Sync Agent não importa flows
```bash
# Remove sentinela para forçar reimportação
rm langflow-flows/.initialized
docker-compose restart sync-agent
```

### Sync Tradutor não converte
```bash
# Verifica logs
docker logs juscrash-sync-tradutor

# Verifica hash
cat langflow-flows/.principal_hash
```

### Código Python inválido gerado
```bash
# Restaura backup
cp backend/app/workflow.py.bak backend/app/workflow.py
```

## 📊 Monitoramento

### Verificar Status
```bash
# Sync Agent
docker exec juscrash-sync-agent ls -la /app/langflow-flows/

# Sync Tradutor
docker exec juscrash-sync-tradutor ls -la /app/backend/app/
```

### Testar Conversão Manual
```bash
# LangGraph → LangFlow
docker exec juscrash-sync-tradutor python -c "from sync_tradutor import langgraph_to_langflow; langgraph_to_langflow()"

# LangFlow → LangGraph
docker exec juscrash-sync-tradutor python -c "from sync_tradutor import langflow_to_langgraph; langflow_to_langgraph()"
```
