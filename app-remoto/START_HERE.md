# 🚀 Bem-vindo ao JUSCRASH App-Remoto!

## ✅ Estrutura Criada com Sucesso!

**29 arquivos** criados para deploy serverless na AWS.

---

## 📖 Por onde começar?

### **1️⃣ Leia a documentação** (5 min)

```bash
# Visão geral
cat README.md

# Deploy rápido
cat QUICKSTART.md

# Checklist completo
cat CHECKLIST.md
```

---

### **2️⃣ Entenda a arquitetura** (10 min)

```
CloudFront → S3 (Frontend)
    ↓
API Gateway
    ↓
Lambda (LangGraph + Bedrock)
    ↓
S3 (Flows JSON)
```

**Arquivos principais:**
- `agent-core/src/handler.py` - Entry point Lambda
- `agent-core/src/graph.py` - LangGraph workflow
- `infrastructure/*.tf` - Terraform IaC

---

### **3️⃣ Faça o deploy** (30 min)

#### **Passo 1: Infraestrutura**
```bash
cd infrastructure

# Criar bucket de state (primeira vez)
aws s3 mb s3://juscrash-terraform-state

# Deploy
terraform init
terraform apply
```

**Copie os outputs:**
- `ecr_repository_url`
- `api_url`
- `cloudfront_distribution_id`

---

#### **Passo 2: Backend**
```bash
cd ../agent-core
chmod +x deploy.sh
./deploy.sh
```

Aguarde ~5 minutos para build e push da imagem.

---

#### **Passo 3: Frontend**
```bash
cd ../../app-local/frontend

# Configurar API URL
echo "VITE_API_URL=<API_URL_DO_TERRAFORM>" > .env.production

# Build e deploy
npm run build
aws s3 sync dist/ s3://juscrash-frontend/ --delete
```

---

### **4️⃣ Teste** (5 min)

#### **Health Check**
```bash
curl https://YOUR_API_URL/health
```

**Esperado:**
```json
{
  "status": "ok",
  "service": "juscrash-agent-core",
  "runtime": "aws-lambda"
}
```

---

#### **Verificar Processo**
```bash
curl -X POST https://YOUR_API_URL/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d @agent-core/test_processo.json
```

**Esperado:**
```json
{
  "decision": "approved",
  "rationale": "...",
  "citacoes": ["POL-1", "POL-2"]
}
```

---

#### **Acessar Frontend**
```
https://xxxxx.cloudfront.net
```

---

## 📚 Documentação Completa

| Arquivo | Quando Ler |
|---------|------------|
| [README.md](./README.md) | Visão geral completa |
| [QUICKSTART.md](./QUICKSTART.md) | Deploy em 3 passos |
| [CHECKLIST.md](./CHECKLIST.md) | Checklist detalhado |
| [SUMMARY.md](./SUMMARY.md) | Resumo do que foi criado |
| [agent-core/README.md](./agent-core/README.md) | Backend Lambda |
| [infrastructure/README.md](./infrastructure/README.md) | Terraform |

---

## 🎯 Estrutura de Pastas

```
app-remoto/
├── agent-core/          ← Backend Lambda (Python + LangGraph)
├── infrastructure/      ← Terraform (IaC)
├── frontend/            ← React App (copiar de app-local)
└── *.md                 ← Documentação
```

---

## 💡 Dicas

### **Primeira vez com AWS?**
1. Configure billing alerts
2. Use região `us-east-1`
3. Monitore custos diariamente nos primeiros dias

### **Primeira vez com Terraform?**
1. Sempre faça `terraform plan` antes de `apply`
2. State file é crítico (está no S3)
3. Use `terraform destroy` para deletar tudo

### **Primeira vez com Lambda?**
1. Logs estão no CloudWatch
2. Cold start pode levar ~5s
3. Timeout padrão é 60s

---

## 🐛 Problemas Comuns

### **Terraform erro: backend not initialized**
```bash
aws s3 mb s3://juscrash-terraform-state
terraform init
```

### **Lambda erro: image not found**
1. Comente `aws_lambda_function` no `lambda.tf`
2. `terraform apply`
3. Execute `./deploy.sh`
4. Descomente e `terraform apply` novamente

### **Frontend não carrega**
```bash
# Invalidar cache CloudFront
aws cloudfront create-invalidation \
  --distribution-id <ID> \
  --paths "/*"
```

---

## 💰 Custos

**Estimativa mensal (uso baixo):**
- S3: $1
- CloudFront: $5
- Lambda: $10
- API Gateway: $0.35
- Bedrock: $15
- **Total: ~$31/mês**

**Configure alertas:**
```bash
aws budgets create-budget \
  --account-id <ACCOUNT_ID> \
  --budget file://budget.json
```

---

## 🎉 Pronto para começar!

**Próximo comando:**
```bash
cd infrastructure
terraform init
```

**Tempo estimado:** 30-45 minutos para deploy completo

**Dúvidas?** Consulte os arquivos README em cada pasta.

---

## 📞 Recursos

- **AWS Docs:** https://docs.aws.amazon.com/
- **Terraform:** https://registry.terraform.io/providers/hashicorp/aws/
- **LangGraph:** https://langchain-ai.github.io/langgraph/
- **Bedrock:** https://docs.aws.amazon.com/bedrock/

---

**Boa sorte! 🚀**

*Criado por José Cleiton*
