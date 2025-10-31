# ⚡ JUSCRASH - Quick Start AWS

Deploy completo em 3 passos.

---

## 🎯 Pré-requisitos

```bash
# AWS CLI configurado
aws configure

# Terraform instalado
terraform --version

# Docker rodando
docker --version
```

---

## 🚀 Deploy em 3 Passos

### **1️⃣ Infraestrutura (5 min)**

```bash
cd infrastructure

# Criar bucket de state (apenas primeira vez)
aws s3 mb s3://juscrash-terraform-state

# Deploy
terraform init
terraform apply
```

**Outputs importantes:**
- `ecr_repository_url` - Copie para usar no passo 2
- `api_url` - Copie para usar no passo 3

---

### **2️⃣ Backend (3 min)**

```bash
cd ../agent-core

# Editar deploy.sh se necessário
chmod +x deploy.sh
./deploy.sh
```

Aguarde o push da imagem e update do Lambda.

---

### **3️⃣ Frontend (2 min)**

```bash
cd ../../app-local/frontend

# Configurar API URL (do passo 1)
echo "VITE_API_URL=<API_URL_DO_TERRAFORM>" > .env.production

# Build e deploy
npm run build
aws s3 sync dist/ s3://juscrash-frontend/ --delete
```

---

## ✅ Testar

### **Health Check**

```bash
curl https://YOUR_API_URL/health
```

**Resposta esperada:**
```json
{
  "status": "ok",
  "service": "juscrash-agent-core",
  "runtime": "aws-lambda"
}
```

---

### **Verificar Processo**

```bash
curl -X POST https://YOUR_API_URL/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d @agent-core/test_processo.json
```

**Resposta esperada:**
```json
{
  "decision": "approved",
  "rationale": "Processo atende todos os critérios...",
  "citacoes": ["POL-1", "POL-2", "POL-7"]
}
```

---

## 🌐 Acessar Frontend

```bash
# Ver URL do CloudFront
cd infrastructure
terraform output frontend_url
```

Acesse a URL no navegador.

---

## 📊 Monitorar

### **Logs do Lambda**

```bash
aws logs tail /aws/lambda/juscrash-agent-core --follow
```

---

### **Métricas**

```bash
# Invocações
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=juscrash-agent-core \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

---

## 🔄 CI/CD (Opcional)

### **Configurar GitHub Actions**

1. Adicione secrets no repositório:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `VITE_API_URL`
   - `CLOUDFRONT_DISTRIBUTION_ID`

2. Push para `main`:

```bash
git add .
git commit -m "feat: deploy AWS"
git push origin main
```

GitHub Actions fará deploy automático.

---

## 🐛 Troubleshooting

### **Lambda não atualiza**

```bash
# Forçar update
aws lambda update-function-code \
  --function-name juscrash-agent-core \
  --image-uri $(terraform output -raw ecr_repository_url):latest
```

---

### **Frontend não carrega**

```bash
# Invalidar cache CloudFront
aws cloudfront create-invalidation \
  --distribution-id $(terraform output -raw cloudfront_distribution_id) \
  --paths "/*"
```

---

### **Bedrock permission denied**

```bash
# Verificar IAM
aws iam get-role-policy \
  --role-name juscrash-lambda-role \
  --policy-name juscrash-lambda-policy
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

---

## 📚 Documentação Completa

- [README Principal](./README.md)
- [Agent Core](./agent-core/README.md)
- [Infrastructure](./infrastructure/README.md)

---

## 🎉 Pronto!

Seu sistema está no ar! 🚀

**URLs:**
- Frontend: `https://xxxxx.cloudfront.net`
- API: `https://xxxxx.execute-api.us-east-1.amazonaws.com/prod`
