# 🧪 Teste do Sync Tradutor

## 🚀 Setup Rápido

### 1. Configure o .env
```bash
cd app-local/sync-agent
cp .env.example .env
# Edite .env com suas credenciais AWS e Agent ID
```

### 2. Instale dependências
```bash
pip install -r requirements.txt
```

### 3. Execute teste único
```bash
python test_tradutor.py
```

---

## 📋 Variáveis Necessárias

No arquivo `.env`:

```bash
# Obrigatórias
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
BEDROCK_AGENT_ID=seu-agent-id

# Opcionais
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
BEDROCK_AGENT_ALIAS_ID=TSTALIASID
```

---

## 🔍 O Que o Teste Faz

1. ✅ Carrega variáveis do `.env` local
2. ✅ Exibe configurações (modelo, agent, região)
3. ✅ Lê `juscash_flow.json`
4. ✅ Invoca Bedrock Agent para traduzir
5. ✅ Valida código com Code Interpreter
6. ✅ Cria backup e substitui `workflow.py`

---

## 📊 Logs Esperados

```
🧪 Teste do Sync Tradutor
============================================================
AWS_REGION: us-east-1
BEDROCK_MODEL_ID: anthropic.claude-3-5-sonnet-20240620-v1:0
BEDROCK_AGENT_ID: XXXXXXXXXX
============================================================

🚀 Executando tradução única...

[14:30:15] 🔄 Iniciando tradução...
[14:30:15] 🤖 Invocando Bedrock Agent...
[14:30:15] 🧠 Modelo: anthropic.claude-3-5-sonnet-20240620-v1:0
[14:30:18] ✅ Resposta recebida (2543 chars)
[14:30:18] 🧪 Iniciando validação...
[14:30:21] ✅ Validação: PASSOU
[14:30:21] 💾 Criando backup...
[14:30:21] ✅ workflow.py atualizado

✅ Teste concluído com sucesso!
```

---

## ⚠️ Troubleshooting

### Agent ID não configurado
```
⚠️  BEDROCK_AGENT_ID não configurado - Tradutor desabilitado
```
**Solução:** Configure `BEDROCK_AGENT_ID` no `.env`

### Erro de credenciais AWS
```
❌ Erro ao invocar agent: UnrecognizedClientException
```
**Solução:** Verifique `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`

### Arquivo não encontrado
```
❌ FileNotFoundError: juscash_flow.json
```
**Solução:** Execute de dentro da pasta `sync-agent` ou ajuste caminhos

---

## 🎯 Próximos Passos

Após teste bem-sucedido:

1. Integre no Docker Compose
2. Configure watch loop automático
3. Monitore logs em produção
