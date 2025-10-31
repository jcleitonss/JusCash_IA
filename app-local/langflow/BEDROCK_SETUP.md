# 🔧 Configurar AWS Bedrock no LangFlow

## ✅ Credenciais Já Configuradas

As credenciais AWS já estão no `docker-compose.yml`:

```yaml
environment:
  - AWS_ACCESS_KEY_ID=AKIAQF53QHFGBNVOHXMC
  - AWS_SECRET_ACCESS_KEY=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
  - AWS_DEFAULT_REGION=us-east-1
  - BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
```

---

## 🚀 Como Usar no LangFlow

### 1. Inicie o LangFlow
```bash
cd app-local/langflow
docker compose up
```

### 2. Acesse
http://localhost:7860

### 3. Configure o Componente Amazon Bedrock

**No flow, configure o componente `Amazon Bedrock` com:**

| Campo | Valor |
|-------|-------|
| **Model ID** | `anthropic.claude-3-5-sonnet-20240620-v1:0` |
| **Region Name** | `us-east-1` |
| **AWS Access Key ID** | `AWS_ACCESS_KEY_ID` (deixe assim) |
| **AWS Secret Access Key** | `AWS_SECRET_ACCESS_KEY` (deixe assim) |

**Importante:** Deixe os campos de credenciais com os **nomes das variáveis**, não cole as chaves diretamente!

---

## 🎯 Modelos Disponíveis

```
anthropic.claude-3-5-sonnet-20241022-v2:0  ← Mais recente
anthropic.claude-3-5-sonnet-20240620-v1:0  ← Atual (configurado)
anthropic.claude-3-5-haiku-20241022-v1:0   ← Mais rápido/barato
anthropic.claude-3-haiku-20240307-v1:0     ← Mais barato
```

---

## 🔄 Trocar o Agent para Bedrock

**Atualmente o Agent usa OpenAI. Para trocar:**

1. No componente **Agent**, clique em **Model Provider**
2. Selecione **"Connect other models"**
3. Conecte o componente **Amazon Bedrock** → **Agent** (entrada "Language Model")
4. Remova a conexão com OpenAI

---

## ✅ Testar

1. Cole dados de um processo no **Chat Input**
2. Execute o flow
3. Veja a resposta no **Chat Output**

---

## 🔍 Verificar Logs

```bash
docker logs -f langflow
```

Se houver erro de credenciais, você verá no log.

---

## 🛡️ Segurança

⚠️ **NUNCA commite o `docker-compose.yml` com credenciais!**

Para produção, use:
```yaml
environment:
  - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
  - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
```

E crie um `.env` file (não commitado).
