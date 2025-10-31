# 🤖 JUSCRASH Agent Core

Backend serverless rodando em AWS Lambda com LangGraph + Bedrock Claude 3.

---

## 🏗️ Arquitetura

```
API Gateway
    ↓
Lambda (este código)
    ↓
LangGraph Workflow
    ├─ validate_node (POL-1 a POL-8)
    ├─ analyze_node (Bedrock Claude)
    └─ decision_node (resultado)
```

---

## 📁 Estrutura

```
agent-core/
├── src/
│   ├── chains/
│   │   ├── policy_chain.py    # Validação POL-1 a POL-8
│   │   └── llm_chain.py       # Bedrock Claude 3
│   ├── graph.py               # LangGraph workflow
│   ├── handler.py             # Lambda entry point
│   └── models.py              # Pydantic models
├── Dockerfile                 # Lambda container
├── requirements.txt
├── deploy.sh                  # Script de deploy
└── README.md
```

---

## 🚀 Deploy

### **Pré-requisitos**

```bash
# AWS CLI configurado
aws configure

# Docker rodando
docker --version

# Terraform já aplicado (ECR + Lambda criados)
```

---

### **Deploy Rápido**

```bash
chmod +x deploy.sh
./deploy.sh
```

O script irá:
1. ✅ Build da imagem Docker
2. ✅ Login no ECR
3. ✅ Push da imagem
4. ✅ Update do Lambda

---

## 🧪 Testes

### **Local (Docker)**

```bash
# Build
docker build -t juscrash-agent-core .

# Run local
docker run -p 9000:8080 \
  -e AWS_ACCESS_KEY_ID=xxx \
  -e AWS_SECRET_ACCESS_KEY=xxx \
  juscrash-agent-core

# Test
curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations \
  -d '{"body": "{\"numeroProcesso\": \"test\"}"}'
```

---

### **AWS Lambda**

```bash
# Invocar diretamente
aws lambda invoke \
  --function-name juscrash-agent-core \
  --payload '{"httpMethod": "GET", "path": "/health"}' \
  response.json

cat response.json
```

---

### **Via API Gateway**

```bash
# Health check
curl https://YOUR_API_URL/health

# Verificar processo
curl -X POST https://YOUR_API_URL/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d @test_processo.json
```

---

## 📊 Monitoramento

### **CloudWatch Logs**

```bash
# Logs em tempo real
aws logs tail /aws/lambda/juscrash-agent-core --follow

# Últimas 100 linhas
aws logs tail /aws/lambda/juscrash-agent-core --since 1h
```

---

### **Métricas**

```bash
# Invocações
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=juscrash-agent-core \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum

# Erros
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=juscrash-agent-core \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

---

## 🔧 Configuração

### **Variáveis de Ambiente (Lambda)**

```bash
FLOWS_BUCKET=juscrash-flows
AWS_BEDROCK_REGION=us-east-1
```

Configurar via Terraform ou AWS Console.

---

### **Timeout e Memória**

```bash
# Aumentar timeout
aws lambda update-function-configuration \
  --function-name juscrash-agent-core \
  --timeout 120

# Aumentar memória
aws lambda update-function-configuration \
  --function-name juscrash-agent-core \
  --memory-size 2048
```

---

## 🐛 Troubleshooting

### **Erro: Bedrock permission denied**

```bash
# Verificar IAM role
aws iam get-role-policy \
  --role-name juscrash-lambda \
  --policy-name lambda_custom

# Adicionar permissão
aws iam put-role-policy \
  --role-name juscrash-lambda \
  --policy-name bedrock-access \
  --policy-document '{
    "Statement": [{
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "*"
    }]
  }'
```

---

### **Erro: Lambda timeout**

```bash
# Aumentar timeout para 120s
aws lambda update-function-configuration \
  --function-name juscrash-agent-core \
  --timeout 120
```

---

### **Erro: Out of memory**

```bash
# Aumentar memória para 2GB
aws lambda update-function-configuration \
  --function-name juscrash-agent-core \
  --memory-size 2048
```

---

## 📚 Referências

- **LangGraph:** https://langchain-ai.github.io/langgraph/
- **AWS Bedrock:** https://docs.aws.amazon.com/bedrock/
- **Lambda Containers:** https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
- **Mangum:** https://mangum.io/

---

## 💰 Custos

| Componente | Custo |
|------------|-------|
| Lambda (10k requests × 1GB × 5s) | $10/mês |
| Bedrock (1M tokens) | $15/mês |
| ECR (500 MB) | $0.05/mês |
| **Total** | **~$25/mês** |

---

## 🔄 CI/CD

Deploy automático via GitHub Actions quando fizer push na branch `main`.

Ver: `../../.github/workflows/deploy.yml`
