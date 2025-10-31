# 🔐 Setup AWS Bedrock

A chave que você tem (`bedrock-long-term-api-key.csv`) é uma **API Key do Bedrock**, não credenciais IAM padrão.

---

## ❌ Problema Atual

A API Key do Bedrock tem formato diferente das credenciais AWS tradicionais (Access Key + Secret Key).

---

## ✅ Solução: Usar AWS CLI Configure

### **Opção 1: Criar IAM User (Recomendado)**

1. **Acesse o Console AWS**
   - https://console.aws.amazon.com/

2. **Vá para IAM → Users → Create user**
   - Nome: `juscrash-bedrock-user`

3. **Attach policies:**
   - `AmazonBedrockFullAccess`

4. **Security credentials → Create access key**
   - Use case: Application running outside AWS
   - Copie: `Access Key ID` e `Secret Access Key`

5. **Configure AWS CLI:**
```bash
aws configure
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: ...
# Default region: us-east-1
# Default output format: json
```

---

### **Opção 2: Usar variáveis de ambiente**

Crie arquivo `.env` em `app-local/backend/`:

```bash
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-20250929-v1:0
```

---

### **Opção 3: Usar AWS SSO (se sua empresa usa)**

```bash
aws sso login
aws sso configure
```

---

## 🧪 Testar

Depois de configurar:

```bash
# Testar AWS CLI
aws bedrock list-foundation-models --region us-east-1

# Testar API
python test_connection.py
```

---

## 📝 Nota sobre a API Key atual

A chave em `bedrock-long-term-api-key.csv` parece ser:
- Uma API Key do Bedrock (não IAM)
- Formato: `BedrockAPIKey-xxx-at-account:secret`

Esse formato **não é suportado** pelo boto3/langchain diretamente.

Você precisa de **credenciais IAM** (Access Key + Secret Key) para usar o Bedrock via SDK.

---

## 🆘 Precisa de ajuda?

Se você não tem acesso para criar IAM user, peça ao administrador AWS da sua conta.
