# ⚡ Quick Start - JUSCRASH Backend

Guia rápido para rodar a API localmente.

---

## 🚀 Passo a Passo

### **1. Instalar dependências**

```bash
cd app-local/backend
pip install -r requirements.txt
```

---

### **2. Testar conexão com Bedrock**

```bash
python test_connection.py
```

**Saída esperada:**
```
==================================================
🧪 TESTE DE CONEXÃO - JUSCRASH API
==================================================

🔧 Testando configurações...
✅ API Key carregada: ABSKQmVkcm9ja0FQSUt...
✅ Região: us-east-1
✅ Modelo: anthropic.claude-3-sonnet-20240229-v1:0

🤖 Testando conexão com Bedrock...
✅ Resposta do Bedrock: OK

==================================================
✅ Testes concluídos!
==================================================
```

---

### **3. Rodar a API**

```bash
uvicorn app.main:app --reload --port 8000
```

**Saída esperada:**
```
🚀 Iniciando JUSCRASH API...
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### **4. Testar endpoints**

#### **Health check:**
```bash
curl http://localhost:8000/health
```

**Resposta:**
```json
{
  "status": "ok",
  "service": "juscrash-api",
  "version": "1.0.0"
}
```

#### **Documentação interativa:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 Testar análise de processo

### **Criar arquivo de teste:**

```bash
# Criar pasta data
mkdir ../../data

# Criar processo_teste.json
```

```json
{
  "numeroProcesso": "0001234-56.2023.4.05.8100",
  "classe": "Cumprimento de Sentença",
  "orgaoJulgador": "19ª VARA FEDERAL",
  "ultimaDistribuicao": "2024-11-18T23:15:44.130Z",
  "assunto": "Rural",
  "segredoJustica": false,
  "justicaGratuita": true,
  "siglaTribunal": "TRF5",
  "esfera": "Federal",
  "documentos": [
    {
      "id": "DOC-1",
      "dataHoraJuntada": "2023-09-10T10:12:05.000Z",
      "nome": "Certidão de Trânsito em Julgado",
      "texto": "Certifico que a sentença transitou em julgado."
    }
  ],
  "movimentos": [
    {
      "dataHora": "2024-01-20T11:22:33.000Z",
      "descricao": "Iniciado cumprimento definitivo de sentença."
    }
  ]
}
```

### **Enviar request:**

```bash
curl -X POST http://localhost:8000/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d @../../data/processo_teste.json
```

**Resposta esperada:**
```json
{
  "decision": "approved",
  "rationale": "Processo transitado em julgado e em fase de execução...",
  "citacoes": ["POL-1", "POL-2"]
}
```

---

## 🐛 Troubleshooting

### **Erro: Module not found**
```bash
pip install -r requirements.txt
```

### **Erro: Bedrock access denied**
- Verifique se a chave está correta em `app-local/keys/bedrock-long-term-api-key.csv`
- Confirme que o modelo Claude 3 está habilitado na sua conta AWS

### **Erro: Import error config**
- Verifique se o arquivo `app-local/keys/config.py` existe
- Confirme que o CSV da chave está na pasta `keys/`

---

## 📚 Próximos passos

1. ✅ API rodando localmente
2. ⏭️ Testar com os 11 processos exemplo
3. ⏭️ Integrar com frontend React
4. ⏭️ Adicionar LangFuse (observabilidade)
5. ⏭️ Deploy com Docker

---

## 🆘 Precisa de ajuda?

- Documentação: http://localhost:8000/docs
- README completo: [README.md](README.md)
