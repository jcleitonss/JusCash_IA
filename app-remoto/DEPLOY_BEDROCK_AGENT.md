# 🤖 Deploy JUSCRASH com Bedrock Agent

## 🎯 Arquitetura

```
Frontend (S3 + CloudFront)
    ↓
API Gateway
    ↓
Lambda (LangGraph)
    ↓
Bedrock Agent Runtime
    ↓
Bedrock Agent (Claude 3.5 Sonnet)
```

---

## 📋 Pré-requisitos

1. **AWS CLI configurado**
2. **Docker rodando**
3. **Credenciais em `keys/.env`**

---

## 🚀 Deploy Completo

### **Passo 1: Verificar credenciais**

```bash
cat keys/.env
```

Deve conter:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`

---

### **Passo 2: Deploy Infraestrutura (Terraform)**

```bash
cd app-remoto/infrastructure

# Inicializar Terraform
docker compose -f docker-compose.deploy.yml run terraform-init

# Ver o que será criado
docker compose -f docker-compose.deploy.yml run terraform-plan

# Criar recursos AWS
docker compose -f docker-compose.deploy.yml run terraform-apply
```

**Recursos criados:**
- ✅ Bedrock Agent
- ✅ Agent Alias (production)
- ✅ Lambda Function
- ✅ ECR Repository
- ✅ API Gateway
- ✅ S3 Buckets
- ✅ CloudFront
- ✅ IAM Roles

---

### **Passo 3: Pegar IDs do Bedrock Agent**

```bash
cd app-remoto/infrastructure

# Ver outputs
docker compose -f docker-compose.deploy.yml run terraform-output

# Copiar:
# - bedrock_agent_id
# - bedrock_agent_alias_id
```

---

### **Passo 4: Configurar variáveis de ambiente**

Adicione no `keys/.env`:

```bash
BEDROCK_AGENT_ID=XXXXXXXXXX
BEDROCK_AGENT_ALIAS_ID=XXXXXXXXXX
```

---

### **Passo 5: Deploy Backend (Lambda)**

```bash
cd app-remoto/infrastructure

# Build + Push Docker + Update Lambda
docker compose -f docker-compose.deploy.yml run deploy-backend
```

---

### **Passo 6: Deploy Frontend**

```bash
cd app-remoto/infrastructure

# Build React + Upload S3
docker compose -f docker-compose.deploy.yml run deploy-frontend
```

---

## ✅ Testar

### **1. Health Check**

```bash
curl https://SEU_API_URL/health
```

Resposta esperada:
```json
{
  "status": "ok",
  "service": "juscrash-agent-core",
  "runtime": "aws-lambda",
  "bedrock_agent": {
    "agent_id": "XXXXXXXXXX",
    "agent_alias_id": "XXXXXXXXXX",
    "region": "us-east-1",
    "configured": true
  }
}
```

---

### **2. Verificar Processo**

```bash
curl -X POST https://SEU_API_URL/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d '{
    "numeroProcesso": "0001234-56.2023.4.05.8100",
    "classe": "Cumprimento de Sentença",
    "orgaoJulgador": "19ª VARA FEDERAL",
    "ultimaDistribuicao": "2023-01-01T00:00:00",
    "assunto": "Indenização",
    "segredoJustica": false,
    "justicaGratuita": false,
    "siglaTribunal": "TRF5",
    "esfera": "Federal",
    "documentos": [],
    "movimentos": []
  }'
```

---

## 🔄 Atualizar

### **Atualizar código do Lambda:**

```bash
cd app-remoto/infrastructure
docker compose -f docker-compose.deploy.yml run deploy-backend
```

### **Atualizar frontend:**

```bash
cd app-remoto/infrastructure
docker compose -f docker-compose.deploy.yml run deploy-frontend
```

---

## 🐛 Troubleshooting

### **Erro: BEDROCK_AGENT_ID não configurado**

Adicione no `keys/.env`:
```bash
BEDROCK_AGENT_ID=XXXXXXXXXX
BEDROCK_AGENT_ALIAS_ID=XXXXXXXXXX
```

### **Erro: Permission denied (Bedrock Agent)**

Verifique IAM role do Lambda:
```bash
aws iam get-role-policy \
  --role-name juscrash-lambda-role \
  --policy-name juscrash-lambda-policy
```

Deve ter permissões:
- `bedrock:InvokeAgent`
- `bedrock:GetAgent`

### **Ver logs do Lambda:**

```bash
aws logs tail /aws/lambda/juscrash-agent-core --follow
```

---

## 💰 Custos Estimados

| Serviço | Custo Mensal |
|---------|--------------|
| Bedrock Agent | $0 (pay-per-use) |
| Bedrock Claude 3.5 | $15/1M tokens |
| Lambda | $10/10k requests |
| API Gateway | $0.35/10k requests |
| S3 + CloudFront | $5 |
| **Total** | **~$30/mês** |

---

## 📚 Documentação

- **Bedrock Agents:** https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html
- **LangGraph:** https://langchain-ai.github.io/langgraph/
- **Terraform AWS:** https://registry.terraform.io/providers/hashicorp/aws/

---

## ✨ Próximos Passos

- [ ] Adicionar Knowledge Base (RAG)
- [ ] Configurar Guardrails
- [ ] Adicionar Code Interpreter
- [ ] Implementar memória de sessão
- [ ] Custom domain (Route 53)
