# 🐛 Troubleshooting - JUSCASH

Resolução de problemas comuns.

---

## 🔐 Credenciais

### **Erro: Bedrock access denied**

**Causa:** Credenciais inválidas ou modelo não habilitado

**Solução:**
```bash
# 1. Verificar credenciais
cat keys/.env | grep AWS_ACCESS_KEY_ID

# 2. Testar AWS CLI
aws sts get-caller-identity

# 3. Verificar modelo habilitado
aws bedrock list-foundation-models --region us-east-1
```

📖 **Ver:** [../setup/AWS_SETUP.md](../setup/AWS_SETUP.md)

---

### **Erro: GITHUB_TOKEN not found**

**Solução:**
```bash
# Verificar
cat keys/.env | grep GITHUB_TOKEN

# Gerar novo token
# https://github.com/settings/tokens
```

---

## 🐳 Docker

### **Erro: Port already in use**

**Solução:**
```bash
# Parar containers antigos
docker-compose down
docker ps -a
docker rm -f $(docker ps -aq)

# Ou mudar porta no docker-compose.yml
ports:
  - "8001:8000"  # Usar 8001 ao invés de 8000
```

---

### **Erro: Docker daemon not running**

**Solução:**
1. Abrir Docker Desktop
2. Aguardar inicialização
3. Tentar novamente

---

### **Erro: Build failed**

**Solução:**
```bash
# Rebuild sem cache
docker-compose build --no-cache
docker-compose up
```

---

## ⚡ Lambda

### **Erro: Lambda not updating**

**Solução:**
```bash
cd app-remoto/infrastructure
make deploy-backend

# Ou forçar
aws lambda update-function-code \
  --function-name juscrash-agent-core \
  --zip-file fileb://../agent-core/lambda-package.zip
```

---

### **Erro: Lambda timeout**

**Solução:**
```bash
# Aumentar timeout no Terraform
# lambda.tf
timeout = 120  # 2 minutos
```

---

## ☁️ CloudFront

### **Erro: Frontend não carrega**

**Solução:**
```bash
# Invalidar cache
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

---

### **Erro: CloudFront takes too long**

**Causa:** CloudFront demora 15-20 minutos para provisionar

**Solução:** Aguardar ou verificar status:
```bash
aws cloudfront get-distribution --id E1234567890ABC
```

---

## 🏗️ Terraform

### **Erro: State locked**

**Solução:**
```bash
# Forçar unlock
terraform force-unlock <LOCK_ID>
```

---

### **Erro: Resource already exists**

**Solução:**
```bash
# Importar recurso existente
terraform import aws_s3_bucket.frontend juscrash-frontend
```

---

### **Erro: Backend not initialized**

**Solução:**
```bash
# Criar bucket de state
aws s3 mb s3://juscrash-terraform-state

# Reinicializar
terraform init
```

---

## 🔄 Git

### **Erro: Merge conflict**

**Solução:**
```bash
# Ver conflitos
git status

# Resolver manualmente
vim <arquivo_conflito>

# Commitar
git add .
git commit -m "fix: resolve conflicts"
```

---

### **Erro: Permission denied (push)**

**Solução:**
```bash
# Verificar token
cat keys/.env | grep GITHUB_TOKEN

# Gerar novo token
# https://github.com/settings/tokens
```

---

## 🎨 LangFlow

### **Erro: Flow não salva**

**Solução:**
```bash
# Verificar permissões
chmod -R 777 app-local/langflow-flows/

# Reiniciar LangFlow
docker-compose restart langflow
```

---

### **Erro: Bedrock component not found**

**Solução:**
1. Atualizar LangFlow: `docker-compose pull langflow`
2. Ou usar componente "Custom"

---

## 📊 API

### **Erro: 502 Bad Gateway**

**Causa:** Backend não está rodando

**Solução:**
```bash
# Verificar backend
docker-compose ps backend

# Reiniciar
docker-compose restart backend
```

---

### **Erro: CORS**

**Solução:**
```bash
# Verificar CORS no backend
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 💰 Custos

### **Erro: Custos muito altos**

**Solução:**
```bash
# Ver custos por serviço
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

# Reduzir custos:
# 1. Usar Claude Haiku (mais barato)
# 2. Reduzir timeout Lambda
# 3. Usar CloudFront cache
```

---

## 🆘 Ainda com Problemas?

1. **Ver logs:**
   ```bash
   # Local
   docker-compose logs -f
   
   # AWS
   make logs
   ```

2. **Verificar status:**
   ```bash
   make status
   ```

3. **Testar API:**
   ```bash
   make test-api
   ```

4. **Abrir issue:** https://github.com/jcleitonss/JusCash_IA/issues

---

## 📚 Referências

- [Setup Local](../setup/LOCAL_SETUP.md)
- [Deploy AWS](../deploy/QUICKSTART.md)
- [API Examples](API_EXAMPLES.md)
