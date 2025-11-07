# 🔐 Setup AWS Bedrock - JUSCASH

Guia para configurar credenciais AWS e habilitar Bedrock.

---

## 🎯 O que você precisa

- Conta AWS ativa
- Permissões para criar IAM users
- Acesso ao Bedrock (Claude)

---

## 📋 Passo a Passo

### **1. Habilitar Bedrock**

1. Acesse: https://console.aws.amazon.com/bedrock
2. Vá em **Model access**
3. Clique em **Manage model access**
4. Selecione:
   - ✅ **Claude 3.5 Sonnet**
   - ✅ **Claude 3.5 Haiku** (opcional)
5. Clique em **Request model access**
6. Aguarde aprovação (geralmente instantâneo)

---

### **2. Criar IAM User**

1. Acesse: https://console.aws.amazon.com/iam
2. **Users** → **Create user**
3. Nome: `juscrash-bedrock-user`
4. **Next**

---

### **3. Adicionar Permissões**

**Attach policies:**
- ✅ `AmazonBedrockFullAccess`
- ✅ `AmazonS3FullAccess` (se usar S3)

Ou criar policy customizada:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "*"
    }
  ]
}
```

---

### **4. Criar Access Key**

1. Clique no user criado
2. **Security credentials**
3. **Create access key**
4. Use case: **Application running outside AWS**
5. **Next** → **Create access key**
6. **Copie:**
   - `Access Key ID` (ex: AKIA...)
   - `Secret Access Key` (ex: wJalrXUt...)

⚠️ **Salve em local seguro! Não será mostrado novamente.**

---

### **5. Configurar no Projeto**

Edite `keys/.env`:

```bash
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=wJalrXUt...
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-20250929-v1:0
```

---

## 🧪 Testar Conexão

### **Opção 1: AWS CLI**

```bash
aws bedrock list-foundation-models --region us-east-1
```

### **Opção 2: Script Python**

```bash
cd app-local/backend
python test_connection.py
```

**Saída esperada:**
```
✅ API Key carregada
✅ Região: us-east-1
✅ Modelo: anthropic.claude-sonnet-4-5-20250929-v1:0
✅ Resposta do Bedrock: OK
```

---

## 🔐 Segurança

### **Boas Práticas**

✅ **Nunca commitar credenciais**
- `keys/.env` está no `.gitignore`

✅ **Rotacionar chaves periodicamente**
```bash
aws iam create-access-key --user-name juscrash-bedrock-user
aws iam delete-access-key --access-key-id AKIA... --user-name juscrash-bedrock-user
```

✅ **Usar IAM roles em produção**
- Lambda usa roles, não access keys
- Deploy via Lambda ZIP (não usa ECR)

---

## 🌍 Regiões Disponíveis

| Região | Código | Latência BR |
|--------|--------|-------------|
| **N. Virginia** | `us-east-1` | ~150ms ✅ |
| **Oregon** | `us-west-2` | ~200ms |
| **São Paulo** | `sa-east-1` | ~20ms ⚠️ Bedrock não disponível |

**Recomendado:** `us-east-1` (melhor custo/latência)

---

## 💰 Custos Bedrock

| Modelo | Input (1M tokens) | Output (1M tokens) |
|--------|-------------------|-------------------|
| **Claude 3.5 Sonnet** | $3.00 | $15.00 |
| **Claude 3.5 Haiku** | $0.80 | $4.00 |

**Exemplo:** Análise de 10k processos/mês
- Input: 10k × 10k tokens = 100M tokens = $300
- Output: 10k × 500 tokens = 5M tokens = $75
- **Total:** ~$375/mês

---

## 🐛 Troubleshooting

### **Erro: Model access denied**
- Verifique se solicitou acesso ao modelo no console Bedrock
- Aguarde aprovação (pode levar alguns minutos)

### **Erro: Invalid credentials**
- Confirme que copiou Access Key e Secret corretamente
- Verifique se não há espaços extras

### **Erro: Region not supported**
- Bedrock não está disponível em todas as regiões
- Use `us-east-1` ou `us-west-2`

---

## 📚 Referências

- **Bedrock Console:** https://console.aws.amazon.com/bedrock
- **IAM Console:** https://console.aws.amazon.com/iam
- **Pricing:** https://aws.amazon.com/bedrock/pricing/
- **Docs:** https://docs.aws.amazon.com/bedrock/
