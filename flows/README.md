# 📁 Flows JSON (Fonte de Verdade)

Flows do LangFlow exportados e versionados no Git.

---

## 🎯 O que é isso?

Esta pasta contém os workflows (flows) criados visualmente no LangFlow e exportados como JSON.

- ✅ **Fonte de verdade** - Versionado no Git
- ✅ **Sincronizado** - Deploy automático para S3
- ✅ **Executável** - Usado pelo Lambda em produção

---

## 🔄 Fluxo

```
LangFlow (local)
    ↓
Sync Agent exporta
    ↓
flows/*.json (Git)
    ↓
GitHub Actions
    ↓
S3 (juscrash-flows)
    ↓
Lambda carrega e executa
```

---

## 📝 Estrutura de um Flow

```json
{
  "name": "Decision Flow",
  "description": "Analisa processos judiciais",
  "data": {
    "nodes": [
      {
        "id": "input-1",
        "type": "ChatInput"
      },
      {
        "id": "bedrock-1",
        "type": "AmazonBedrock",
        "data": {
          "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0"
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

## 🚀 Como Usar

### **1. Criar flow no LangFlow (local)**

```bash
cd app-local/langflow
docker compose up
# Acesse http://localhost:7860
```

---

### **2. Exportar para Git**

O Sync Agent exporta automaticamente para `app-local/langflow-flows/`.

Copie para esta pasta:

```bash
cp app-local/langflow-flows/decision_flow.json flows/
```

---

### **3. Commit e Push**

```bash
git add flows/
git commit -m "feat: novo flow de decisão"
git push origin main
```

---

### **4. Deploy Automático**

GitHub Actions detecta mudança e sincroniza com S3:

```bash
# Automático via GitHub Actions
flows/ → S3 (juscrash-flows)
```

---

## 📊 Flows Disponíveis

Adicione seus flows aqui:

- `decision_flow.json` - Decisão de compra de crédito
- `validation_flow.json` - Validação de políticas
- `analysis_flow.json` - Análise com LLM

---

## 🔧 Comandos Úteis

### **Validar JSON**

```bash
cat flows/decision_flow.json | jq empty
```

---

### **Ver flows no S3**

```bash
aws s3 ls s3://juscrash-flows/
```

---

### **Sync manual para S3**

```bash
aws s3 sync flows/ s3://juscrash-flows/ --delete
```

---

## 📚 Referências

- **LangFlow Docs:** https://docs.langflow.org/
- **Sync Agent:** [../app-local/SYNC_AGENT_GUIDE.md](../app-local/SYNC_AGENT_GUIDE.md)
