# 🐳 Setup Local - JUSCASH

Guia completo para rodar o projeto localmente com Docker.

---

## 🎯 Pré-requisitos

- **Docker Desktop** 20.10+
- **Docker Compose** 2.0+
- **Conta AWS** com Bedrock habilitado

---

## ⚡ Quick Start

```bash
cd app-local
docker-compose up --build
```

**Acesse:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- LangFlow: http://localhost:7860

---

## 🔧 Configuração Detalhada

### **1. Configurar Credenciais AWS**

Edite `keys/.env`:

```bash
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-20250929-v1:0
```

📖 **Ver:** [AWS_SETUP.md](AWS_SETUP.md)

---

### **2. Testar Conexão Bedrock**

```bash
cd app-local/backend
python test_connection.py
```

**Saída esperada:**
```
✅ API Key carregada
✅ Região: us-east-1
✅ Resposta do Bedrock: OK
```

---

### **3. Subir Serviços**

```bash
cd app-local
docker-compose up --build
```

**Serviços iniciados:**
- ✅ Backend FastAPI (porta 8000)
- ✅ Frontend React (porta 5173)
- ✅ LangFlow (porta 7860)
- ✅ Sync Agent (background)

---

## 🧪 Testar API

### **Health Check**

```bash
curl http://localhost:8000/health
```

### **Verificar Processo**

```bash
curl -X POST http://localhost:8000/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d @data/processo_teste.json
```

---

## 📊 Documentação Interativa

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🎨 LangFlow Editor

**Acesse:** http://localhost:7860

**Fluxo de Sincronização:**
1. Edita workflow no LangFlow → Salva no PostgreSQL
2. Sync Agent exporta para `langflow-flows/workflow.json` (60s)
3. Sync Tradutor traduz JSON → Python via Claude 4.5
4. Backend atualizado automaticamente

📚 **Ver:** [LANGFLOW_SETUP.md](LANGFLOW_SETUP.md) | [SYNC_FLOW.md](../SYNC_FLOW.md)

---

## 🛑 Parar Serviços

```bash
docker-compose down
```

---

## 🐛 Troubleshooting

### **Erro: Bedrock access denied**
- Verifique credenciais em `keys/.env`
- Confirme que Claude está habilitado no console AWS

### **Erro: Port already in use**
```bash
# Parar containers antigos
docker-compose down
docker ps -a
docker rm -f <container_id>
```

### **Erro: Module not found**
```bash
# Rebuild containers
docker-compose up --build
```

---

## 📚 Próximos Passos

- ✅ Ambiente local rodando
- ⏭️ [Configurar LangFlow](LANGFLOW_SETUP.md)
- ⏭️ [Entender Sincronização](../SYNC_FLOW.md)
- ⏭️ [Deploy AWS](../deploy/QUICKSTART.md)

---

**Autor:** José Cleiton  
**Projeto:** JUSCASH  
**Versão:** 1.0
