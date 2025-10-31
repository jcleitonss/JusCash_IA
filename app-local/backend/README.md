# 🚀 JUSCRASH Backend API

API FastAPI para verificação inteligente de processos judiciais usando LangGraph + AWS Bedrock + S3.

---

## 🏗️ Arquitetura

```
┌──────────────────────────────────────────────┐
│              FastAPI (porta 8000)            │
│  ├─ /health                                  │
│  ├─ /api/v1/verificar                        │
│  └─ /api/v1/resultado/{numero}               │
└────────────────┬─────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────┐
│         LangGraph Workflow (Python)          │
│  ├─ Nó 1: Validar Políticas                 │
│  ├─ Nó 2: Análise LLM (Bedrock)             │
│  └─ Nó 3: Salvar Resultado (S3)             │
└────────────────┬─────────────────────────────┘
                 │
                 ├──────────────┬───────────────┐
                 ▼              ▼               ▼
         ┌──────────┐   ┌──────────┐   ┌──────────┐
         │  Bedrock │   │    S3    │   │ LangFuse │
         │ (Claude) │   │  (AWS)   │   │  (Obs.)  │
         └──────────┘   └──────────┘   └──────────┘
```

---

## 📁 Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + endpoints
│   ├── models.py            # Pydantic models (Processo, Documento, etc)
│   ├── graph.py             # LangGraph workflow (Python)
│   ├── llm_service.py       # LangChain + AWS Bedrock
│   ├── policy_checker.py    # Validações POL-1 a POL-8
│   ├── s3_service.py        # Integração AWS S3
│   └── observability.py     # LangFuse setup
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## 🎯 Decisões Técnicas

### **Por que Python para LangGraph?**
✅ Controle total do fluxo  
✅ Mais rápido (sem parsing de JSON)  
✅ Fácil debug e testes  
✅ Integração nativa com LangChain  
✅ Versionamento via Git  

### **Por que AWS Bedrock?**
✅ Claude 3 (Sonnet/Opus) - excelente para análise jurídica  
✅ Sem gerenciar chaves OpenAI  
✅ Integração nativa AWS (S3, IAM)  
✅ Custo otimizado  
✅ Latência baixa (região AWS)  

### **Por que S3?**
✅ Armazenamento durável  
✅ Organização por data (YYYY/MM/DD)  
✅ Metadados para busca  
✅ Versionamento automático  
✅ Integração com outros serviços AWS  

---

## 🔧 Pré-requisitos

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Conta AWS** com:
  - Bedrock habilitado (Claude 3)
  - S3 bucket criado
  - IAM user com permissões

---

## ⚙️ Configuração

### **1. Criar bucket S3**

```bash
aws s3 mb s3://juscrash-results --region us-east-1
```

### **2. Habilitar Bedrock**

No console AWS:
- Acesse **Amazon Bedrock**
- Vá em **Model access**
- Solicite acesso ao **Claude 3 Sonnet**

### **3. Criar IAM User**

Permissões necessárias:
- `bedrock:InvokeModel`
- `s3:PutObject`
- `s3:GetObject`

### **4. Configurar variáveis de ambiente**

```bash
cp .env.example .env
# Edite .env com suas credenciais
```

---

## 🚀 Como Rodar

### **Opção 1: Docker (Recomendado)**

```bash
# Build
docker build -t juscrash-api .

# Run
docker run -p 8000:8000 --env-file .env juscrash-api
```

### **Opção 2: Docker Compose**

```bash
# Do diretório app-local (raiz)
cd ..
docker-compose up backend --build

# Ou apenas backend isolado
docker-compose up backend
```

### **Opção 3: Local (Desenvolvimento)**

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar
uvicorn app.main:app --reload --port 8000
```

---

## 🌐 Endpoints

### **GET /health**
Health check da API

**Response:**
```json
{
  "status": "ok",
  "service": "juscrash-api",
  "s3_bucket": "juscrash-results"
}
```

---

### **POST /api/v1/verificar**
Verifica processo judicial conforme políticas POL-1 a POL-8

**Request:**
```json
{
  "numeroProcesso": "0001234-56.2023.4.05.8100",
  "classe": "Cumprimento de Sentença contra a Fazenda Pública",
  "orgaoJulgador": "19ª VARA FEDERAL - SOBRAL/CE",
  "ultimaDistribuicao": "2024-11-18T23:15:44.130Z",
  "assunto": "Rural (Art. 48/51)",
  "segredoJustica": false,
  "justicaGratuita": true,
  "siglaTribunal": "TRF5",
  "esfera": "Federal",
  "documentos": [...],
  "movimentos": [...]
}
```

**Response:**
```json
{
  "decision": "approved",
  "rationale": "Processo transitado em julgado e em fase de execução. Valor de condenação R$ 67.592,00 atende ao mínimo. Documentação completa.",
  "citacoes": ["POL-1", "POL-2"],
  "s3_key": "resultados/2024/01/15/0001234-56.2023.4.05.8100.json"
}
```

**Possíveis decisões:**
- `approved` - Processo aprovado para compra
- `rejected` - Processo rejeitado
- `incomplete` - Documentação incompleta

---

### **GET /api/v1/resultado/{numero_processo}**
Busca resultado já processado no S3

**Response:**
```json
{
  "numeroProcesso": "0001234-56.2023.4.05.8100",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "decision": "approved",
  "rationale": "...",
  "citacoes": ["POL-1", "POL-2"],
  "metadata": {
    "processed_at": "2024-01-15T10:30:00.000Z",
    "version": "1.0"
  }
}
```

---

## 📜 Políticas de Negócio

| ID | Regra | Ação |
|----|-------|------|
| **POL-1** | Transitado em julgado + fase de execução | Obrigatório |
| **POL-2** | Valor de condenação informado | Obrigatório |
| **POL-3** | Valor < R$ 1.000 | Rejeitar |
| **POL-4** | Esfera trabalhista | Rejeitar |
| **POL-5** | Óbito sem inventário | Rejeitar |
| **POL-6** | Substabelecimento sem reserva | Rejeitar |
| **POL-7** | Informar honorários | Obrigatório |
| **POL-8** | Documento essencial faltando | Incompleto |

---

## 🔄 Fluxo do LangGraph

```
┌─────────────────────┐
│  Recebe Processo    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Valida Políticas    │ ← POL-3, POL-4 (auto-reject)
│ (policy_checker.py) │
└──────────┬──────────┘
           │
           ▼
      ┌────────┐
      │ Rejeitado │ ─── Sim ──→ [Retorna rejected]
      │ auto?     │
      └────┬─────┘
           │ Não
           ▼
┌─────────────────────┐
│  Análise LLM        │ ← Bedrock Claude 3
│  (llm_service.py)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Salva no S3        │ ← s3://juscrash-results/
│  (s3_service.py)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Retorna Decisão     │
└─────────────────────┘
```

---

## 🧪 Testes

### **Testar endpoint de verificação:**

```bash
curl -X POST http://localhost:8000/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d @../../data/processos_exemplo.json
```

### **Testar busca no S3:**

```bash
curl http://localhost:8000/api/v1/resultado/0001234-56.2023.4.05.8100
```

### **Verificar health:**

```bash
curl http://localhost:8000/health
```

---

## 📊 Observabilidade

### **LangFuse Dashboard**
- Acesse: https://cloud.langfuse.com
- Veja traces de cada request
- Monitore latência e custos
- Debug prompts e respostas

### **Logs**
```bash
# Ver logs do container
docker logs -f juscrash-api

# Logs em tempo real
docker-compose logs -f juscrash-api
```

---

## 🔐 Variáveis de Ambiente

```bash
# AWS Bedrock
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

# AWS S3
S3_BUCKET_NAME=juscrash-results

# LangFuse (Observabilidade)
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_HOST=https://cloud.langfuse.com

# API
LOG_LEVEL=INFO
```

---

## 📦 Dependências Principais

```txt
fastapi==0.109.0           # API REST
uvicorn==0.27.0            # ASGI server
pydantic==2.5.0            # Validação de dados
langchain==0.1.0           # Framework LLM
langchain-aws==0.1.0       # Integração Bedrock
langgraph==0.0.20          # Workflow orchestration
langfuse==2.6.0            # Observabilidade
boto3==1.34.0              # AWS SDK
```

---

## 🐳 Docker

### **Build:**
```bash
docker build -t juscrash-api:latest .
```

### **Run:**
```bash
docker run -d \
  --name juscrash-api \
  -p 8000:8000 \
  --env-file .env \
  juscrash-api:latest
```

### **Stop:**
```bash
docker stop juscrash-api
docker rm juscrash-api
```

---

## 🔍 Troubleshooting

### **Erro: Bedrock access denied**
- Verifique se o modelo Claude 3 está habilitado no console AWS
- Confirme permissões IAM: `bedrock:InvokeModel`

### **Erro: S3 bucket not found**
- Crie o bucket: `aws s3 mb s3://juscrash-results`
- Verifique região: bucket e API devem estar na mesma região

### **Erro: LangFuse connection failed**
- Verifique chaves em https://cloud.langfuse.com
- Confirme que LANGFUSE_HOST está correto

---

## 📚 Documentação

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 🚀 Próximos Passos

1. ✅ Implementar models.py (Pydantic schemas)
2. ✅ Implementar policy_checker.py (validações)
3. ✅ Implementar llm_service.py (Bedrock + LangChain)
4. ✅ Implementar s3_service.py (upload/download)
5. ✅ Implementar graph.py (LangGraph workflow)
6. ✅ Implementar main.py (FastAPI endpoints)
7. ✅ Criar Dockerfile
8. ✅ Testar com 11 processos exemplo

---

## 👤 Autor

**José Cleiton**

---

## 📅 Prazo

7 dias corridos
