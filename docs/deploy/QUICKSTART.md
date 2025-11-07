# ⚡ Quick Start - Deploy AWS

Deploy completo em 3 passos.

---

## 🎯 Pré-requisitos

- Docker Desktop rodando
- Credenciais AWS configuradas em `keys/.env`

---

## 🚀 Deploy em 3 Passos

### **1️⃣ Inicializar Terraform (5 min)**

```bash
cd app-remoto/infrastructure
make init
```

---

### **2️⃣ Criar Infraestrutura (15 min)**

```bash
make apply
```

Aguarde criação de:
- CloudFront (demora ~15 min)
- Lambda, API Gateway, S3

---

### **3️⃣ Deploy Aplicação (3 min)**

```bash
make deploy
```

Faz:
- Build Lambda
- Build React
- Sync S3
- Invalidate CloudFront

---

## ✅ Testar

### **Ver URLs**

```bash
make output
```

**Saída:**
```
frontend_url = "https://d26fvod1jq9hfb.cloudfront.net"
api_url = "https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod"
```

---

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
  -d @app-remoto/agent-core/test_processo.json
```

---

## 📊 Monitorar

```bash
# Logs em tempo real
make logs

# Status AWS
make status

# Testar API
make test-api
```

---

## 🔄 Atualizar

```bash
# Atualizar código
make deploy

# Atualizar infraestrutura
make plan
make apply
```

---

## 🐛 Troubleshooting

### **Erro: Credentials not found**

```bash
# Verificar
cat ../../keys/.env

# Reconfigurar
aws configure
```

### **Erro: CloudFront takes too long**

CloudFront demora 15-20 minutos. Aguarde ou use:

```bash
# Ver status
aws cloudfront get-distribution --id <DISTRIBUTION_ID>
```

### **Erro: Lambda not updating**

```bash
# Forçar update
make deploy-backend
```

---

## 📚 Próximos Passos

- **Backend detalhado:** [BACKEND.md](BACKEND.md)
- **Frontend detalhado:** [FRONTEND.md](FRONTEND.md)
- **Terraform completo:** [TERRAFORM.md](TERRAFORM.md)
- **Git workflow:** [GIT_WORKFLOW.md](GIT_WORKFLOW.md)

---

**Autor:** José Cleiton  
**Projeto:** JUSCASH  
**Versão:** 1.0
