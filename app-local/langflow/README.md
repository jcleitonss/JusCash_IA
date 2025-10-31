# 🎨 LangFlow - Editor Visual de Workflows

Interface visual drag-and-drop para criar e editar workflows de LLM.

---

## 🚀 Iniciar

```bash
cd app-local/langflow
docker compose up
```

---

## 🌐 Acessar

**URL:** http://localhost:7860

---

## 🎯 Funcionalidades

### **Editor Visual**
- ✅ Drag-and-drop de componentes
- ✅ Conectar nós visualmente
- ✅ Testar em tempo real
- ✅ Exportar código Python

### **Componentes Disponíveis**
- 🤖 LLMs (OpenAI, Anthropic, AWS Bedrock)
- 📝 Prompts e Templates
- 🔗 Chains e Agents
- 💾 Memory e Vector Stores
- 🔧 Tools e Utilities

---

## 🔧 Configuração AWS Bedrock

✅ **Credenciais já configuradas no `docker-compose.yml`**

1. **Acesse:** http://localhost:7860
2. **Crie novo Flow**
3. **Adicione componente:** `Amazon Bedrock`
4. **Configure:**
   - Model ID: `anthropic.claude-3-5-sonnet-20240620-v1:0`
   - Region: `us-east-1`
   - AWS Access Key ID: `AWS_ACCESS_KEY_ID` (deixe assim)
   - AWS Secret Access Key: `AWS_SECRET_ACCESS_KEY` (deixe assim)

**Importante:** O LangFlow busca automaticamente as credenciais das variáveis de ambiente!

📖 **Guia completo:** [BEDROCK_SETUP.md](BEDROCK_SETUP.md)

---

## 📊 Recriar Workflow JUSCRASH

### **Estrutura:**

```
┌──────────────┐
│ Input        │ (Dados do processo)
└──────┬───────┘
       │
┌──────▼───────┐
│ Validate     │ (POL-1 a POL-8)
└──────┬───────┘
       │
       ├─ rejected ──► ┌────────┐
       │                │ Output │
       │                └────────┘
       │
       └─ approved ──► ┌─────────┐
                       │ Bedrock │ (Claude)
                       └────┬────┘
                            │
                       ┌────▼────┐
                       │ Output  │
                       └─────────┘
```

### **Passos:**

1. **Input Node** - Recebe JSON do processo
2. **Python Function** - Valida políticas (POL-1 a POL-8)
3. **Conditional Router** - Decide se continua ou rejeita
4. **Amazon Bedrock** - Análise com Claude
5. **Output Node** - Retorna decisão

---

## 💾 Exportar/Importar Flows

### **Exportar:**
- Clique em `⋮` → `Export`
- Salva arquivo `.json`

### **Importar:**
- Clique em `Import`
- Selecione arquivo `.json`

---

## 🔌 Integrar com Backend

LangFlow expõe API REST:

```bash
# Executar flow
curl -X POST http://localhost:7860/api/v1/run/{flow_id} \
  -H "Content-Type: application/json" \
  -d '{"input": {...}}'
```

---

## 🛑 Parar

```bash
docker compose down
```

---

## 📚 Documentação

- **LangFlow:** https://docs.langflow.org/
- **GitHub:** https://github.com/logspace-ai/langflow
- **Componentes:** https://docs.langflow.org/components/

---

## 🆚 LangFlow vs LangGraph

| Recurso | LangFlow | LangGraph |
|---------|----------|-----------|
| **Editor Visual** | ✅ Completo | ⚠️ Limitado |
| **Drag-and-drop** | ✅ | ❌ |
| **Code-first** | ⚠️ | ✅ |
| **Controle Fino** | ⚠️ | ✅ |
| **Prototipagem** | ✅ Rápida | ⚠️ Lenta |
| **Produção** | ✅ | ✅ |

---

## 💡 Próximos Passos

1. ✅ LangFlow rodando
2. ⏭️ Acesse http://localhost:7860
3. ⏭️ Crie novo Flow
4. ⏭️ Recrie workflow JUSCRASH visualmente
5. ⏭️ Teste e exporte código
