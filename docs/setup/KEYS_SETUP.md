# 🔐 Gerenciamento de Chaves - JUSCASH

Guia para gerenciar credenciais e chaves do projeto.

---

## 📁 Estrutura

```
keys/
├── .env                    # Credenciais (NÃO commitado)
├── .gitignore              # Protege .env
└── README.md               # Este arquivo
```

---

## 🔧 Configurar Credenciais

### **1. Criar arquivo `.env`**

```bash
cd keys
cp .env.example .env
```

---

### **2. Editar `keys/.env`**

```bash
# ========================================
# AWS CREDENTIALS
# ========================================
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# ========================================
# AWS BEDROCK (LLM)
# ========================================
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-20250929-v1:0

# ========================================
# LANGSMITH (Observabilidade)
# ========================================
LANGSMITH_API_KEY=lsv2_pt_...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=juscrash
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# ========================================
# GITHUB (Versionamento)
# ========================================
GITHUB_TOKEN=ghp_...
GITHUB_USER=seu_usuario
GITHUB_REPO=JUSCRASH
```

---

## 🔑 Obter Credenciais

### **AWS Access Keys**

1. Console AWS → IAM → Users
2. Selecione user → Security credentials
3. Create access key
4. Copie `Access Key ID` e `Secret Access Key`

📖 **Ver:** [AWS_SETUP.md](AWS_SETUP.md)

---

### **LangSmith API Key**

1. Acesse: https://smith.langchain.com
2. Settings → API Keys
3. Create API Key
4. Copie `LANGSMITH_API_KEY`

---

### **GitHub Token**

1. GitHub → Settings → Developer settings
2. Personal access tokens → Generate new token
3. Permissões: `repo` (full control)
4. Copie token

---

## 🔐 Segurança

### **Boas Práticas**

✅ **NUNCA commitar `.env`**
```bash
# Já está no .gitignore
keys/.env
```

✅ **Rotacionar chaves periodicamente**
```bash
# A cada 90 dias
aws iam create-access-key --user-name juscrash-user
```

✅ **Usar variáveis de ambiente**
```bash
# Docker Compose lê automaticamente
docker-compose up
```

✅ **Permissões mínimas (IAM)**
- Apenas `bedrock:InvokeModel`
- Apenas `s3:GetObject` no bucket específico

---

## 🧪 Testar Credenciais

### **AWS**

```bash
aws sts get-caller-identity
```

### **Bedrock**

```bash
cd app-local/backend
python test_connection.py
```

### **GitHub**

```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

---

## 🔄 Compartilhar com Equipe

### **Opção 1: Gerenciador de Senhas**

Use 1Password, LastPass, Bitwarden para compartilhar `.env`

---

### **Opção 2: AWS Secrets Manager**

```bash
# Salvar
aws secretsmanager create-secret \
  --name juscrash/credentials \
  --secret-string file://keys/.env

# Recuperar
aws secretsmanager get-secret-value \
  --secret-id juscrash/credentials \
  --query SecretString \
  --output text > keys/.env
```

---

### **Opção 3: Variáveis de Ambiente CI/CD**

GitHub Actions:
1. Repo → Settings → Secrets
2. Add secret para cada variável
3. Usa `${{ secrets.AWS_ACCESS_KEY_ID }}`

---

## 🗑️ Revogar Credenciais

### **AWS Access Key**

```bash
aws iam delete-access-key \
  --access-key-id AKIA... \
  --user-name juscrash-user
```

### **GitHub Token**

1. GitHub → Settings → Developer settings
2. Personal access tokens
3. Delete token

### **LangSmith**

1. https://smith.langchain.com
2. Settings → API Keys
3. Revoke key

---

## 📋 Checklist de Segurança

- [ ] `.env` está no `.gitignore`
- [ ] Credenciais não estão no código
- [ ] IAM user tem permissões mínimas
- [ ] Chaves rotacionadas a cada 90 dias
- [ ] Secrets não estão em logs
- [ ] Variáveis de ambiente em produção

---

## 🐛 Troubleshooting

### **Erro: Credentials not found**

```bash
# Verificar se .env existe
ls -la keys/.env

# Verificar conteúdo
cat keys/.env | grep AWS_ACCESS_KEY_ID
```

### **Erro: Permission denied**

```bash
# Verificar permissões IAM
aws iam get-user-policy \
  --user-name juscrash-user \
  --policy-name BedrockAccess
```

---

## 📚 Referências

- **AWS IAM:** https://console.aws.amazon.com/iam
- **LangSmith:** https://smith.langchain.com
- **GitHub Tokens:** https://github.com/settings/tokens
