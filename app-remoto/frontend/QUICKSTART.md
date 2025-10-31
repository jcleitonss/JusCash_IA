# ⚡ Frontend - Deploy Rápido

## Opção 1: Só S3 (mais rápido)

```bash
# 1. Criar bucket
aws s3 mb s3://juscrash-frontend --region us-east-1

# 2. Configurar como site
aws s3 website s3://juscrash-frontend --index-document index.html --error-document index.html

# 3. Tornar público
aws s3api put-bucket-policy --bucket juscrash-frontend --policy file://bucket-policy.json

# 4. Build e deploy
cd app-remoto/frontend
npm install
echo VITE_API_URL=https://API_GATEWAY_URL > .env.production
npm run build
aws s3 sync dist/ s3://juscrash-frontend/ --delete
```

**URL:** http://juscrash-frontend.s3-website-us-east-1.amazonaws.com

---

## Opção 2: S3 + CloudFront (com Terraform)

```bash
cd app-remoto/infrastructure
terraform init
terraform apply
```

Depois faça o build e deploy do frontend.

---

## 🔄 Atualizar frontend

```bash
npm run build
aws s3 sync dist/ s3://juscrash-frontend/ --delete
```
