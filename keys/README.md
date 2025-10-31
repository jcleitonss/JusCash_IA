# 🔐 JUSCASH - Credenciais Centralizadas

Esta pasta contém TODAS as credenciais do projeto:
- AWS (deploy infraestrutura)
- GitHub (versionamento automatizado)
- LangSmith (observabilidade)

---

## 📁 Estrutura

```
keys/
├── .env                # Todas as credenciais (PRINCIPAL)
├── .gitkeep
└── README.md           # Este arquivo
```

⚠️ **IMPORTANTE:** `keys/.env` está no `.gitignore` e NUNCA deve ser commitado!

---

## 🔧 Configurar Credenciais

### **1. AWS Credentials**

```bash
# Pegar no AWS Console → IAM → Users → Security Credentials
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

### **2. GitHub Token**

```bash
# Pegar em: https://github.com/settings/tokens
# Permissões: repo (Full control)
GITHUB_TOKEN=ghp_...
GITHUB_USER=seu_usuario
GITHUB_REPO=JusCash_AI
```

### **3. LangSmith (Opcional)**

```bash
# Pegar em: https://smith.langchain.com/settings
LANGSMITH_API_KEY=lsv2_pt_...
LANGSMITH_PROJECT=seu_projeto
```

### **Arquivo Completo: `keys/.env`**

Ver exemplo em `.env` (já configurado)

---

## ⚠️ Segurança

- ✅ Esta pasta está no `.gitignore`
- ✅ Nunca commite credenciais no Git
- ✅ Use IAM roles em produção
- ✅ Rotacione chaves regularmente

---

## 🧪 Testar Credenciais

### **AWS:**
```bash
# Carregar .env e testar
source keys/.env
aws sts get-caller-identity
```

### **GitHub:**
```bash
# Testar token
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

### **Makefile (automático):**
```bash
cd app-remoto/infrastructure
make version  # Carrega keys/.env automaticamente
```

---

## 📋 Permissões Necessárias

Sua conta AWS precisa de:
- ✅ S3 (criar buckets, upload)
- ✅ Lambda (criar functions, update code)
- ✅ ECR (criar repositories, push images)
- ✅ API Gateway (criar APIs)
- ✅ CloudFront (criar distributions)
- ✅ IAM (criar roles, policies)
- ✅ CloudWatch (logs)

**Recomendado:** Use `AdministratorAccess` para testes.

---

## 🔄 Rotação de Chaves

```bash
# 1. Criar nova chave no AWS Console
# 2. Atualizar keys/credentials
# 3. Testar
docker run --rm -v ./keys:/root/.aws:ro amazon/aws-cli sts get-caller-identity

# 4. Deletar chave antiga no AWS Console
```

---

## 🆘 Troubleshooting

### **Erro: Unable to locate credentials**

```bash
# Verificar se arquivos existem
ls -la keys/

# Reconfigurar
docker run --rm -it -v ./keys:/root/.aws amazon/aws-cli configure
```

### **Erro: Access Denied**

Sua conta não tem permissões suficientes. Adicione policies no IAM.

---

## 📚 Referências

- **AWS CLI Config:** https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
- **IAM Best Practices:** https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
