# ✅ Checklist de Deploy AWS

---

## 📋 Pré-Deploy

### **AWS Account**
- [ ] Conta AWS criada
- [ ] AWS CLI instalado e configurado (`aws configure`)
- [ ] Credenciais com permissões adequadas
- [ ] Região definida (us-east-1)

### **Ferramentas**
- [ ] Terraform instalado (`terraform --version`)
- [ ] Docker instalado e rodando (`docker --version`)
- [ ] Node.js 18+ instalado (`node --version`)
- [ ] Git configurado

### **Custos**
- [ ] Billing alerts configurados
- [ ] Budget definido (~$50/mês)
- [ ] Entendimento dos custos AWS

---

## 🏗️ Deploy Infraestrutura

### **1. Backend S3 (State)**
- [ ] Criar bucket: `aws s3 mb s3://juscrash-terraform-state`
- [ ] Habilitar versionamento
- [ ] Confirmar bucket criado: `aws s3 ls | grep terraform`

### **2. Terraform Init**
```bash
cd app-remoto/infrastructure
terraform init
```
- [ ] Backend inicializado
- [ ] Providers baixados
- [ ] Sem erros

### **3. Terraform Plan**
```bash
terraform plan
```
- [ ] Revisar recursos a serem criados
- [ ] Confirmar custos estimados
- [ ] Sem erros de validação

### **4. Terraform Apply**
```bash
terraform apply
```
- [ ] Confirmar com `yes`
- [ ] Aguardar conclusão (~15-20 min)
- [ ] Copiar outputs:
  - [ ] `ecr_repository_url`
  - [ ] `api_url`
  - [ ] `frontend_url`
  - [ ] `cloudfront_distribution_id`

### **5. Validar Recursos**
```bash
# Lambda
aws lambda get-function --function-name juscrash-agent-core

# ECR
aws ecr describe-repositories --repository-names juscrash-agent-core

# S3
aws s3 ls | grep juscrash

# CloudFront
aws cloudfront list-distributions
```
- [ ] Lambda criado (sem código ainda)
- [ ] ECR repository criado
- [ ] S3 buckets criados (frontend + flows)
- [ ] CloudFront distribution criado

---

## 🤖 Deploy Backend (Lambda)

### **1. Build Docker**
```bash
cd ../agent-core
docker build -t juscrash-agent-core .
```
- [ ] Build sem erros
- [ ] Imagem criada

### **2. Login ECR**
```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```
- [ ] Login successful

### **3. Push Imagem**
```bash
./deploy.sh
```
- [ ] Imagem tagged
- [ ] Push para ECR concluído
- [ ] Lambda atualizado

### **4. Testar Lambda**
```bash
# Health check
curl <API_URL>/health

# Verificar processo
curl -X POST <API_URL>/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d @test_processo.json
```
- [ ] Health check retorna 200
- [ ] API processa requisição
- [ ] Resposta JSON válida

### **5. Verificar Logs**
```bash
aws logs tail /aws/lambda/juscrash-agent-core --follow
```
- [ ] Logs aparecem
- [ ] Sem erros críticos
- [ ] Bedrock respondendo

---

## 🎨 Deploy Frontend

### **1. Configurar Variáveis**
```bash
cd ../../app-local/frontend
echo "VITE_API_URL=<API_URL>" > .env.production
```
- [ ] `.env.production` criado
- [ ] API_URL correto

### **2. Build React**
```bash
npm ci
npm run build
```
- [ ] Build sem erros
- [ ] Pasta `dist/` criada

### **3. Sync S3**
```bash
aws s3 sync dist/ s3://juscrash-frontend/ --delete
```
- [ ] Arquivos enviados
- [ ] Sem erros

### **4. Invalidar CloudFront**
```bash
aws cloudfront create-invalidation \
  --distribution-id <CLOUDFRONT_ID> \
  --paths "/*"
```
- [ ] Invalidação criada
- [ ] Aguardar conclusão (~5 min)

### **5. Testar Frontend**
- [ ] Acessar `<CLOUDFRONT_URL>`
- [ ] Página carrega
- [ ] Formulário aparece
- [ ] Consegue enviar requisição
- [ ] Resposta aparece

---

## 🔄 CI/CD (Opcional)

### **1. GitHub Secrets**
Adicionar no repositório:
- [ ] `AWS_ACCESS_KEY_ID`
- [ ] `AWS_SECRET_ACCESS_KEY`
- [ ] `VITE_API_URL`
- [ ] `CLOUDFRONT_DISTRIBUTION_ID`

### **2. Testar Workflow**
```bash
git add .
git commit -m "test: CI/CD"
git push origin main
```
- [ ] GitHub Actions executou
- [ ] Deploy backend OK
- [ ] Deploy frontend OK
- [ ] Sem erros

---

## 📊 Monitoramento

### **1. CloudWatch**
- [ ] Logs do Lambda visíveis
- [ ] Logs do API Gateway visíveis
- [ ] Métricas aparecendo

### **2. Custos**
- [ ] Cost Explorer configurado
- [ ] Alertas de billing ativos
- [ ] Monitorar primeiros dias

---

## 🧪 Testes Finais

### **API**
- [ ] Health check funciona
- [ ] POST /api/v1/verificar funciona
- [ ] Erros retornam 4xx/5xx apropriados
- [ ] CORS configurado

### **Frontend**
- [ ] Página carrega rápido (<2s)
- [ ] Formulário funciona
- [ ] Resposta aparece
- [ ] Erros são tratados

### **Integração**
- [ ] Frontend → API Gateway → Lambda → Bedrock
- [ ] Fluxo completo funciona
- [ ] Latência aceitável (<5s)

---

## 🐛 Troubleshooting

### **Lambda não responde**
- [ ] Verificar logs CloudWatch
- [ ] Verificar IAM permissions
- [ ] Verificar timeout (60s)
- [ ] Verificar memória (1024 MB)

### **Bedrock erro**
- [ ] Verificar IAM role tem `bedrock:InvokeModel`
- [ ] Verificar região (us-east-1)
- [ ] Verificar model ID correto

### **Frontend não carrega**
- [ ] Verificar S3 bucket policy
- [ ] Verificar CloudFront OAI
- [ ] Invalidar cache CloudFront
- [ ] Verificar CORS

---

## ✅ Deploy Completo!

Quando todos os itens estiverem marcados:

🎉 **Sistema no ar!**

**URLs:**
- Frontend: `https://xxxxx.cloudfront.net`
- API: `https://xxxxx.execute-api.us-east-1.amazonaws.com/prod`

---

## 📚 Próximos Passos

- [ ] Adicionar LangSmith (observabilidade)
- [ ] Configurar custom domain
- [ ] Adicionar WAF (segurança)
- [ ] Implementar cache DynamoDB
- [ ] Adicionar mais flows
- [ ] Documentar APIs (Swagger)
