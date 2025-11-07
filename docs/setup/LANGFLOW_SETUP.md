# 🎨 Setup LangFlow - JUSCASH

Configurar editor visual de workflows LLM.

---

## 🚀 Iniciar LangFlow

```bash
cd app-local
docker-compose up
```

**Serviços iniciados:**
- 🎨 LangFlow (porta 7860)
- 🗄️ PostgreSQL (banco de dados)
- 🔄 Sync Agent (sincronização)
- 🔧 Sync Tradutor (tradução IA)

**Acesse:** http://localhost:7860

---

## 🔧 Configurar AWS Bedrock

### **1. Criar Novo Flow**

1. Clique em **New Flow**
2. Nome: `JUSCASH Decision Flow`

---

### **2. Adicionar Componente Bedrock**

1. Arraste **Amazon Bedrock** para o canvas
2. Configure:

| Campo | Valor |
|-------|-------|
| **Model ID** | `anthropic.claude-sonnet-4-5-20250929-v1:0` |
| **Region** | `us-east-1` |
| **AWS Access Key ID** | `AWS_ACCESS_KEY_ID` |
| **AWS Secret Access Key** | `AWS_SECRET_ACCESS_KEY` |

⚠️ **Importante:** Deixe os campos de credenciais com os **nomes das variáveis**, não cole as chaves!

---

### **3. Testar Conexão**

1. Adicione **Chat Input** → **Amazon Bedrock** → **Chat Output**
2. Digite: "Olá, você está funcionando?"
3. Execute o flow
4. Veja resposta do Claude

---

## 🎯 Criar Workflow JUSCASH

### **Estrutura:**

```
┌──────────────┐
│ Chat Input   │ (Dados do processo)
└──────┬───────┘
       │
┌──────▼───────┐
│ Python Func  │ (Valida POL-1 a POL-8)
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

---

### **Componentes:**

1. **Chat Input** - Recebe JSON do processo
2. **Python Function** - Valida políticas
3. **Conditional Router** - Decide fluxo
4. **Amazon Bedrock** - Análise LLM
5. **Chat Output** - Retorna decisão

---

## 💾 Exportar Flow

**Automático via Sync Agent:**
- Salva no LangFlow → PostgreSQL atualiza
- Sync Agent exporta para `langflow-flows/workflow.json` (60s)
- Sync Tradutor traduz JSON → Python via Claude 4.5
- Backend atualizado automaticamente

> 📚 **Ver:** [SYNC_FLOW.md](../SYNC_FLOW.md) | [SYNC_TRADUTOR.md](../SYNC_TRADUTOR.md)

---

## 🔄 Importar Flow

**Automático via Sync Agent:**
- Adicione `.json` em `langflow-flows/`
- Sync Agent importa para PostgreSQL
- Flow aparece no LangFlow automaticamente

**Manual:**
1. Clique em **Import**
2. Selecione arquivo `.json`
3. Flow carregado no editor

---

## 🧪 Testar Flow

### **Payload de Teste:**

```json
{
  "numeroProcesso": "0001234-56.2023.4.05.8100",
  "classe": "Cumprimento de Sentença",
  "esfera": "Federal",
  "documentos": [
    {
      "nome": "Certidão de Trânsito em Julgado",
      "texto": "Certifico que transitou..."
    }
  ]
}
```

---

## 🎨 Modelos Disponíveis

| Modelo | Uso | Custo |
|--------|-----|-------|
| **Claude 3.5 Sonnet** | Análise complexa | $3/$15 |
| **Claude 3.5 Haiku** | Validações rápidas | $0.8/$4 |

---

## 🐛 Troubleshooting

### **Erro: Bedrock access denied**
- Verifique credenciais em `docker-compose.yml`
- Confirme modelo habilitado no console AWS

### **Erro: Flow não salva**
- Verifique permissões da pasta `langflow-flows/`
- Reinicie LangFlow: `docker compose restart`

---

## 📚 Referências

- **LangFlow Docs:** https://docs.langflow.org/
- **Componentes:** https://docs.langflow.org/components/
- **Bedrock Models:** https://docs.aws.amazon.com/bedrock/
