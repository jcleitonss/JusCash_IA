# 🐳 App Local - JUSCASH

Ambiente de desenvolvimento local com Docker Compose.

---

## 🏗️ Arquitetura Completa

```mermaid
graph TB
    subgraph Docker["🐳 Docker Compose - app-local"]
        subgraph Services["Serviços"]
            LF[🎨 LangFlow<br/>:7860<br/>Editor Visual]:::langflowStyle
            BE[⚙️ Backend<br/>:8000<br/>FastAPI + LangGraph]:::backendStyle
            FE[🖥️ Frontend<br/>:5173<br/>React + MUI]:::frontendStyle
            SA[🔄 Sync Agent<br/>Background<br/>LangFlow ⇄ Git]:::syncStyle
        end
        
        subgraph Storage["Armazenamento"]
            Flows[(📁 langflow-flows/<br/>workflow.json)]:::storageStyle
            Keys[(🔐 keys/<br/>.env)]:::storageStyle
        end
    end
    
    Dev[👨‍💻 Desenvolvedor]:::devStyle --> FE
    Dev --> LF
    Dev --> BE
    
    FE -->|HTTP :8000| BE
    LF -->|Export JSON| SA
    SA -->|Read/Write| Flows
    BE -->|Read Config| Keys
    LF -->|Read Config| Keys
    
    BE -->|Invoke Model| Bedrock[🧠 AWS Bedrock<br/>Claude 3.5]:::awsStyle
    SA -->|Commit/Push| Git[📦 GitHub<br/>Versionamento]:::gitStyle
    
    classDef devStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    classDef langflowStyle fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef backendStyle fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef frontendStyle fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef syncStyle fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef storageStyle fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
    classDef awsStyle fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef gitStyle fill:#333,stroke:#000,stroke-width:2px,color:#fff
```

---

## 📁 Estrutura

```
app-local/
├── backend/          # FastAPI + LangGraph
├── frontend/         # React + Material UI
├── langflow/         # Editor visual de workflows
├── sync-agent/       # Sincronização LangFlow ⇄ Git
├── langflow-flows/   # Workflows exportados (JSON)
├── keys/             # Credenciais AWS (não commitado)
└── docker-compose.yml
```

---

## 🚀 Quick Start

```bash
cd app-local
docker-compose up --build
```

**Acesse:**
- 🖥️ **Frontend:** http://localhost:5173
- ⚙️ **Backend:** http://localhost:8000
- 🎨 **LangFlow:** http://localhost:7860
- 📖 **API Docs:** http://localhost:8000/docs

---

## 🔧 Configuração

### **1. Credenciais AWS**

Edite `keys/.env`:

```bash
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-20250929-v1:0
```

📖 **Ver:** [docs/setup/AWS_SETUP.md](../docs/setup/AWS_SETUP.md)

---

### **2. Subir Serviços**

```bash
# Todos os serviços
docker-compose up --build

# Apenas backend
docker-compose up backend

# Apenas frontend
docker-compose up frontend

# Apenas LangFlow
docker-compose up langflow
```

---

## 📦 Serviços

```mermaid
graph LR
    subgraph Frontend["🖥️ Frontend :5173"]
        React[⚛️ React 18]:::reactStyle
        MUI[🎨 Material UI]:::muiStyle
        Vite[⚡ Vite]:::viteStyle
    end
    
    subgraph Backend["⚙️ Backend :8000"]
        FastAPI[🚀 FastAPI]:::fastapiStyle
        LangGraph[🔄 LangGraph]:::langgraphStyle
        Pydantic[✅ Pydantic]:::pydanticStyle
    end
    
    subgraph LangFlow["🎨 LangFlow :7860"]
        Editor[📝 Visual Editor]:::editorStyle
        Export[📤 Export JSON]:::exportStyle
    end
    
    subgraph SyncAgent["🔄 Sync Agent"]
        Monitor[👁️ Monitor Changes]:::monitorStyle
        Sync[🔄 Bidirectional Sync]:::syncStyle2
    end
    
    Frontend -->|POST /verificar| Backend
    Backend -->|Invoke| Bedrock[🧠 Bedrock]:::bedrockStyle
    LangFlow -->|Export| SyncAgent
    SyncAgent -->|Commit| Git[📦 Git]:::gitStyle
    
    classDef reactStyle fill:#61DAFB,stroke:#149ECA,stroke-width:2px,color:#000
    classDef muiStyle fill:#007FFF,stroke:#0059B2,stroke-width:2px,color:#fff
    classDef viteStyle fill:#646CFF,stroke:#535BF2,stroke-width:2px,color:#fff
    classDef fastapiStyle fill:#009688,stroke:#00796B,stroke-width:2px,color:#fff
    classDef langgraphStyle fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef pydanticStyle fill:#E92063,stroke:#C91952,stroke-width:2px,color:#fff
    classDef editorStyle fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef exportStyle fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef monitorStyle fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef syncStyle2 fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef bedrockStyle fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef gitStyle fill:#333,stroke:#000,stroke-width:2px,color:#fff
```

### **Backend (porta 8000)**
- FastAPI + LangGraph
- Análise de processos via Bedrock
- Endpoints REST

### **Frontend (porta 5173)**
- React 18 + Material UI
- Interface para upload de processos
- Visualização de decisões

### **LangFlow (porta 7860)**
- Editor visual drag-and-drop
- Criação de workflows LLM
- Exportação para JSON

### **Sync Agent (background)**
- Sincronização automática LangFlow ⇄ Git
- Monitora mudanças em `langflow-flows/`
- Importa/exporta workflows

---

## 🧪 Testar

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

## 🛑 Parar

```bash
docker-compose down
```

---

## 📊 Logs

```bash
# Todos os serviços
docker-compose logs -f

# Apenas backend
docker-compose logs -f backend

# Apenas frontend
docker-compose logs -f frontend
```

---

## 🐛 Troubleshooting

### **Porta já em uso**

```bash
# Parar containers antigos
docker-compose down
docker ps -a
docker rm -f $(docker ps -aq)
```

### **Erro de build**

```bash
# Rebuild sem cache
docker-compose build --no-cache
docker-compose up
```

### **Bedrock access denied**

- Verifique `keys/.env`
- Confirme modelo habilitado no console AWS

---

## 📚 Documentação Completa

- 📖 [Setup Local](../docs/setup/LOCAL_SETUP.md)
- 🔐 [Setup AWS](../docs/setup/AWS_SETUP.md)
- 🎨 [Setup LangFlow](../docs/setup/LANGFLOW_SETUP.md)
- ⚙️ [Backend](../docs/components/BACKEND.md)
- 🖥️ [Frontend](../docs/components/FRONTEND.md)
