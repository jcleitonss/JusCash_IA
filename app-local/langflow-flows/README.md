# 📁 LangFlow Flows (JSON)

Pasta contendo flows exportados automaticamente do LangFlow pelo **Sync Agent**.

---

## 🎯 O que é isso?

Esta pasta contém arquivos JSON que representam os workflows criados visualmente no LangFlow.

- ✅ **Fonte verdade** - Sincronizado automaticamente com LangFlow
- ✅ **Versionável** - Pode ser commitado no Git
- ✅ **Executável** - Pode ser executado diretamente no código Python
- ✅ **Portável** - Pode ser importado em qualquer instância do LangFlow

---

## 🔄 Como funciona?

```
┌─────────────┐
│  LangFlow   │  Você cria/edita flows visualmente
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Sync Agent  │  Exporta automaticamente a cada 60s
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Esta pasta  │  Arquivos JSON aparecem aqui
└─────────────┘
```

---

## 📝 Estrutura de um flow JSON

```json
{
  "name": "Decision Flow",
  "description": "Analisa processos judiciais",
  "data": {
    "nodes": [
      {
        "id": "input-1",
        "type": "ChatInput",
        "data": {
          "input_value": ""
        }
      },
      {
        "id": "bedrock-1",
        "type": "AmazonBedrock",
        "data": {
          "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
          "temperature": 0.7
        }
      }
    ],
    "edges": [
      {
        "source": "input-1",
        "target": "bedrock-1"
      }
    ]
  }
}
```

---

## 🚀 Como usar

### **1. Criar flow no LangFlow**

```bash
# Acesse
open http://localhost:7860

# Crie flow visualmente
# Salve (Ctrl+S)
```

### **2. Aguardar sincronização (60s)**

```bash
# Ver logs
docker logs -f juscrash-sync-agent

# Output esperado:
# ✅ decision_flow.json (exportado)
```

### **3. Usar no código Python**

```python
from app.chains.flow_runner import run_flow

result = run_flow(
    flow_name="decision_flow",  # Nome do arquivo (sem .json)
    input_data={"processo": {...}}
)
```

---

## 📦 Importar flow para LangFlow

Se você tem um arquivo JSON e quer importá-lo no LangFlow:

1. Acesse: http://localhost:7860
2. Clique em `Import`
3. Selecione o arquivo `.json`
4. Flow aparece no editor

---

## 🔧 Comandos úteis

### **Listar flows**
```bash
ls -la langflow-flows/
```

### **Ver conteúdo de um flow**
```bash
cat langflow-flows/decision_flow.json | jq
```

### **Validar JSON**
```bash
cat langflow-flows/decision_flow.json | jq empty
```

### **Contar flows**
```bash
ls langflow-flows/*.json | wc -l
```

---

## 📊 Flows disponíveis

Os flows serão criados automaticamente quando você:
1. Criar um flow no LangFlow
2. Aguardar 60s para sincronização

Exemplos de flows que você pode criar:
- `decision_flow.json` - Decisão de compra de crédito
- `validation_flow.json` - Validação de políticas
- `analysis_flow.json` - Análise com LLM
- `policy_check_flow.json` - Verificação de regras

---

## 🐛 Troubleshooting

### **Nenhum flow aparece aqui**

1. Verifique se LangFlow está rodando:
   ```bash
   curl http://localhost:7860/api/v1/flows
   ```

2. Verifique se sync-agent está rodando:
   ```bash
   docker ps | grep sync-agent
   ```

3. Ver logs do sync-agent:
   ```bash
   docker logs juscrash-sync-agent
   ```

### **Flow não atualiza**

1. Forçar sincronização:
   ```bash
   docker compose restart sync-agent
   ```

2. Verificar se salvou no LangFlow (Ctrl+S)

---

## 📚 Referências

- **LangFlow Docs:** https://docs.langflow.org/
- **Sync Agent Guide:** [../SYNC_AGENT_GUIDE.md](../SYNC_AGENT_GUIDE.md)
- **Flow Runner:** [../backend/app/chains/flow_runner.py](../backend/app/chains/flow_runner.py)
