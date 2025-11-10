# 🏗️ JUSCASH - Arquitetura e Fluxos

Documentação visual completa da arquitetura, fluxos de dados e decisões técnicas do sistema JUSCRASH.

---

## 📊 1. Arquitetura AWS Serverless

Visão geral da infraestrutura em produção:

```mermaid
graph TB
    User[👤 Usuário]:::userStyle --> CF[☁️ CloudFront CDN<br/>Distribuição Global]:::awsStyle
    CF --> S3[📦 S3 Bucket<br/>Frontend React]:::awsStyle
    S3 --> API[🚪 API Gateway<br/>REST Endpoints]:::awsStyle
    API --> Lambda[⚡ Lambda Function<br/>Agent Core]:::awsStyle
    Lambda --> LG[🔄 LangGraph<br/>Workflow Engine]:::langStyle
    LG --> Bedrock[🧠 AWS Bedrock<br/>Claude 3.5 Sonnet]:::aiStyle
    
    Lambda -.-> LS[📊 LangSmith<br/>Observability]:::obsStyle
    Lambda -.-> CW[📈 CloudWatch<br/>Logs & Metrics]:::awsStyle
    
    classDef userStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    classDef awsStyle fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef langStyle fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef aiStyle fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
    classDef obsStyle fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

**Componentes:**
- **CloudFront:** CDN global com 200+ edge locations
- **S3:** Hospedagem estática do frontend React
- **API Gateway:** Gerenciamento de endpoints REST
- **Lambda:** Execução serverless do Agent Core
- **LangGraph:** Orquestração do workflow de decisão
- **Bedrock:** LLM Claude 3.5 para análise jurídica
- **LangSmith:** Traces e observabilidade
- **CloudWatch:** Logs e métricas AWS

---

## 🔄 2. Fluxo de Decisão LLM

Sequência completa de análise de um processo judicial:

```mermaid
sequenceDiagram
    participant U as 👤 Usuário
    participant F as 🖥️ Frontend
    participant A as 🚪 API Gateway
    participant L as ⚡ Lambda
    participant W as 🔄 LangGraph
    participant B as 🧠 Bedrock Claude
    participant O as 📊 LangSmith

    U->>F: Upload processo.json
    F->>A: POST /api/v1/verificar
    A->>L: Invoke Lambda
    L->>W: Inicia workflow
    
    rect rgb(124, 58, 237, 0.1)
        Note over W,B: Análise LLM
        W->>W: Monta prompt + POL-1 a POL-8
        W->>B: Invoke Claude 3.5
        B->>B: Analisa 200k tokens<br/>Raciocínio jurídico
        B-->>W: JSON estruturado
    end
    
    W->>W: Valida resposta (Pydantic)
    W-->>L: Decision + Rationale
    L->>O: Registra trace
    L-->>A: Response JSON
    A-->>F: 200 OK
    F-->>U: ✅ Decisão exibida
```

**Tempo médio:** ~2-3 segundos  
**Custo por request:** ~$0.002  
**Taxa de sucesso:** >99%

---

## 🎯 3. Workflow LangGraph

Estados e transições do workflow de análise:

```mermaid
stateDiagram-v2
    [*] --> ReceiveProcess: Processo JSON
    
    ReceiveProcess --> ValidateInput: Validação Pydantic
    ValidateInput --> CheckPolicies: Verifica POL-1 a POL-8
    
    CheckPolicies --> AnalyzeLLM: Análise Claude 3.5
    
    state AnalyzeLLM {
        [*] --> BuildPrompt
        BuildPrompt --> InvokeBedrock
        InvokeBedrock --> ParseJSON
        ParseJSON --> ValidateOutput
        ValidateOutput --> [*]
    }
    
    AnalyzeLLM --> Decision
    
    state Decision {
        [*] --> choice
        choice --> Approved: ✅ approved
        choice --> Rejected: ❌ rejected
        choice --> Incomplete: ⚠️ incomplete
    }
    
    Decision --> LogTrace: LangSmith
    LogTrace --> [*]: Retorna resposta
```

**Nós do Workflow:**
1. **ReceiveProcess:** Recebe JSON do processo
2. **ValidateInput:** Validação Pydantic dos campos
3. **CheckPolicies:** Verificação inicial das políticas
4. **AnalyzeLLM:** Análise via Claude 3.5
5. **Decision:** Decisão final estruturada
6. **LogTrace:** Registro no LangSmith

---

## 📜 4. Políticas de Negócio (POL-1 a POL-8)

Árvore de decisão completa:

```mermaid
graph TD
    Start([📄 Processo Judicial]):::startStyle --> POL1{POL-1<br/>Transitado?}
    
    POL1 -->|❌ Não| INC1[⚠️ INCOMPLETE<br/>Falta trânsito]:::incStyle
    POL1 -->|✅ Sim| POL2{POL-2<br/>Valor informado?}
    
    POL2 -->|❌ Não| INC2[⚠️ INCOMPLETE<br/>Falta valor]:::incStyle
    POL2 -->|✅ Sim| POL3{POL-3<br/>Valor ≥ R$ 1.000?}
    
    POL3 -->|❌ Não| REJ1[❌ REJECTED<br/>Valor baixo]:::rejStyle
    POL3 -->|✅ Sim| POL4{POL-4<br/>Trabalhista?}
    
    POL4 -->|✅ Sim| REJ2[❌ REJECTED<br/>Esfera trabalhista]:::rejStyle
    POL4 -->|❌ Não| POL5{POL-5<br/>Óbito sem inventário?}
    
    POL5 -->|✅ Sim| REJ3[❌ REJECTED<br/>Sem habilitação]:::rejStyle
    POL5 -->|❌ Não| POL6{POL-6<br/>Substabelecimento<br/>sem reserva?}
    
    POL6 -->|✅ Sim| REJ4[❌ REJECTED<br/>Sem poderes]:::rejStyle
    POL6 -->|❌ Não| POL7{POL-7<br/>Honorários<br/>informados?}
    
    POL7 -->|❌ Não| INC3[⚠️ INCOMPLETE<br/>Falta honorários]:::incStyle
    POL7 -->|✅ Sim| POL8{POL-8<br/>Docs essenciais<br/>completos?}
    
    POL8 -->|❌ Não| INC4[⚠️ INCOMPLETE<br/>Falta documento]:::incStyle
    POL8 -->|✅ Sim| APR[✅ APPROVED<br/>Processo aprovado]:::appStyle
    
    classDef startStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    classDef appStyle fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
    classDef rejStyle fill:#EF4444,stroke:#DC2626,stroke-width:3px,color:#fff
    classDef incStyle fill:#F59E0B,stroke:#D97706,stroke-width:3px,color:#fff
```

**Decisões Possíveis:**
- ✅ **APPROVED:** Todas as políticas atendidas
- ❌ **REJECTED:** Violação de POL-3, POL-4, POL-5 ou POL-6
- ⚠️ **INCOMPLETE:** Falta de documentação (POL-1, POL-2, POL-7, POL-8)

---

## 🐳 5. Ambiente Local (Docker Compose)

### Arquitetura Local

```mermaid
graph TB
    Dev[👨💻 Desenvolvedor]:::dev
    
    subgraph Docker["🐳 Docker Compose - 6 Containers"]
        direction TB
        
        subgraph UI["Interface"]
            FE[🖥️ Frontend<br/>:5173<br/>React + Vite]:::frontend
            LF[🎨 LangFlow<br/>:7860<br/>Editor Visual]:::langflow
        end
        
        subgraph Core["Core"]
            BE[⚙️ Backend<br/>:8000<br/>FastAPI + LangGraph]:::backend
            PG[(📦 PostgreSQL<br/>LangFlow DB)]:::db
        end
        
        subgraph Sync["Sincronização"]
            SA[🔄 Sync Agent<br/>LangFlow ↔ JSON]:::sync
            ST[🔧 Sync Tradutor<br/>JSON → Python]:::tradutor
        end
    end
    
    Bedrock[🧠 AWS Bedrock<br/>Claude 3.5]:::bedrock
    Git[(📦 Git Repo)]:::git
    FS[(💾 langflow-flows/)]:::fs
    
    Dev -->|Acessa| FE
    Dev -->|Edita workflow| LF
    FE -->|POST /verificar| BE
    BE -->|Invoca| Bedrock
    
    LF <-->|CRUD| PG
    SA <-->|Monitora| PG
    SA <-->|Exporta/Importa| FS
    SA -.->|Commit| Git
    
    ST -->|Lê| FS
    ST -->|Traduz| BE
    ST -->|Invoca| Bedrock
    
    classDef dev fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    classDef frontend fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef backend fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef langflow fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef db fill:#6366F1,stroke:#4338CA,stroke-width:2px,color:#fff
    classDef sync fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef tradutor fill:#EC4899,stroke:#BE185D,stroke-width:2px,color:#fff
    classDef bedrock fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef git fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
    classDef fs fill:#8B5CF6,stroke:#6D28D9,stroke-width:2px,color:#fff
```

### Serviços Disponíveis

| Serviço | Porta | Descrição | URL |
|---------|-------|------------|-----|
| 🖥️ **Frontend** | 5173 | Interface React para upload de processos | http://localhost:5173 |
| ⚙️ **Backend** | 8000 | API FastAPI + LangGraph + Bedrock | http://localhost:8000 |
| 📝 **Docs** | 8000 | Swagger UI interativo | http://localhost:8000/docs |
| 🎨 **LangFlow** | 7860 | Editor visual de workflows | http://localhost:7860 |
| 📦 **PostgreSQL** | 5432 | Banco de dados do LangFlow | - |
| 🔄 **Sync Agent** | - | LangFlow ↔ JSON (bidirecional) | Background |
| 🔧 **Sync Tradutor** | - | JSON → Python (via Claude 4.5) | Background |

### Quick Start

```bash
# 1. Configurar credenciais
cp keys/.env.example keys/.env
vim keys/.env  # Adicionar AWS_ACCESS_KEY_ID, LANGCHAIN_API_KEY

# 2. Subir todos os serviços
cd app-local
docker-compose up --build

# 3. Acessar
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000/docs
# LangFlow: http://localhost:7860
```

### Fluxo de Desenvolvimento

```mermaid
sequenceDiagram
    participant D as 👨💻 Dev
    participant L as 🎨 LangFlow
    participant P as 📦 PostgreSQL
    participant SA as 🔄 Sync Agent
    participant FS as 💾 langflow-flows/
    participant ST as 🔧 Sync Tradutor
    participant B as ⚙️ Backend
    participant AI as 🧠 Claude 4.5

    rect rgb(124, 58, 237, 0.1)
        Note over D,P: 1. Editar Workflow (LangFlow)
        D->>L: Edita workflow (drag-and-drop)
        L->>P: Salva no PostgreSQL
        P-->>L: Confirma
    end

    rect rgb(245, 158, 11, 0.1)
        Note over SA,FS: 2. Sync Agent (Bidirecional)
        SA->>P: Monitora mudanças (60s)
        P-->>SA: Flow atualizado
        SA->>FS: Exporta workflow.json
        FS-->>SA: Salvo
    end

    rect rgb(236, 72, 153, 0.1)
        Note over ST,B: 3. Sync Tradutor (IA)
        ST->>FS: Detecta workflow.json novo
        ST->>AI: Traduz JSON → Python
        AI-->>ST: workflow.py gerado
        ST->>ST: Valida sintaxe
        ST->>B: Atualiza workflow.py
        B-->>ST: Backend recarregado
    end
```

### Comandos Úteis

```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f langflow

# Parar todos os serviços
docker-compose down

# Rebuild específico
docker-compose up --build backend

# Limpar volumes
docker-compose down -v
```

### Variáveis de Ambiente

**Arquivo:** `keys/.env`

```bash
# AWS Bedrock
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0

# LangSmith (Observabilidade)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_...
LANGCHAIN_PROJECT=juscrash-local

# Git (Sync Agent)
GITHUB_TOKEN=ghp_...
GITHUB_USER=seu-usuario
GITHUB_REPO=JusCash_IA
```

### Troubleshooting

| Problema | Solução |
|----------|----------|
| Porta já em uso | `docker-compose down` e verificar processos |
| Erro de credenciais AWS | Verificar `keys/.env` |
| LangFlow não carrega | Aguardar 30s após `docker-compose up` |
| Sync Agent não commita | Verificar `GITHUB_TOKEN` em `keys/.env` |
| Backend timeout | Aumentar `timeout` em `docker-compose.yml` |

---

## 🚀 6. Pipeline de Deploy

Fluxo CI/CD completo:

```mermaid
graph LR
    Dev[👨💻 Developer]:::devStyle --> Git[📦 Git Push]:::gitStyle
    Git --> TF[🏗️ Terraform<br/>Infrastructure]:::tfStyle
    
    TF --> Lambda[⚡ Lambda<br/>Deploy]:::awsStyle
    TF --> S3[📦 S3<br/>Frontend]:::awsStyle
    TF --> API[🚪 API Gateway<br/>Config]:::awsStyle
    TF --> CF[☁️ CloudFront<br/>Distribution]:::awsStyle
    
    Lambda --> Prod[🚀 Produção]:::prodStyle
    S3 --> Prod
    API --> Prod
    CF --> Prod
    
    Prod --> Monitor[📊 Monitoring]:::monStyle
    Monitor --> LS[LangSmith]:::obsStyle
    Monitor --> CW[CloudWatch]:::obsStyle
    
    classDef devStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef gitStyle fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
    classDef tfStyle fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef awsStyle fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef prodStyle fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
    classDef monStyle fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef obsStyle fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

**Comandos:**
```bash
cd app-remoto/infrastructure
make init      # Inicializa Terraform
make deploy    # Deploy completo
make logs      # Ver logs Lambda
```

---

## 💰 7. Breakdown de Custos

Distribuição de custos para 10k requests/mês:

```mermaid
pie title 💰 Custo Mensal (~$26 para 10k requests)
    "Bedrock Claude 3.5" : 15.00
    "Lambda Compute" : 5.00
    "CloudFront CDN" : 5.00
    "API Gateway" : 0.35
    "S3 Storage" : 0.50
```

**Detalhamento:**
- **Bedrock:** $3/1M tokens input + $15/1M tokens output
- **Lambda:** 10k × 1GB × 5s = $5.00
- **CloudFront:** 100 GB transfer = $5.00
- **API Gateway:** 10k requests × $0.000035 = $0.35
- **S3:** Frontend + state = $0.50

---

## 🔍 8. Análise de Tokens (LLM)

Consumo médio por request:

```mermaid
graph LR
    Input[📥 Input]:::inputStyle --> Prompt[System Prompt<br/>~2.000 tokens]:::promptStyle
    Input --> Process[Processo JSON<br/>~3.000 tokens]:::processStyle
    Input --> Docs[Documentos<br/>~5.000 tokens]:::docsStyle
    
    Prompt --> Total[Total Input<br/>~10.000 tokens]:::totalStyle
    Process --> Total
    Docs --> Total
    
    Total --> LLM[🧠 Claude 3.5<br/>Processamento]:::llmStyle
    
    LLM --> Output[📤 Output<br/>~500 tokens]:::outputStyle
    
    classDef inputStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef promptStyle fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef processStyle fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef docsStyle fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef totalStyle fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef llmStyle fill:#FF9900,stroke:#CC7A00,stroke-width:3px,color:#fff
    classDef outputStyle fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

**Custo por Request:**
- Input: 10.000 tokens × $0.003/1k = $0.03
- Output: 500 tokens × $0.015/1k = $0.0075
- **Total:** ~$0.0375 por análise

---

## 📊 9. Observabilidade

### Stack de Monitoramento

```mermaid
graph TB
    User[👤 Usuário]:::user --> CF[☁️ CloudFront]:::aws
    CF --> API[🚪 API Gateway]:::aws
    API --> Lambda[⚡ Lambda]:::aws
    Lambda --> Bedrock[🧠 Bedrock]:::ai
    
    CF -.->|Logs| CFL[📊 CloudFront Logs<br/>Access patterns]:::obs
    API -.->|Logs| CWL[📈 CloudWatch Logs<br/>Requests/Errors]:::obs
    Lambda -.->|Traces| LS[🔍 LangSmith<br/>LLM Analytics]:::langsmith
    Lambda -.->|Metrics| CWM[📉 CloudWatch Metrics<br/>Performance]:::obs
    Bedrock -.->|Usage| BM[💰 Bedrock Metrics<br/>Tokens/Cost]:::obs
    
    CFL --> Dashboard[📊 Unified Dashboard]:::dash
    CWL --> Dashboard
    LS --> Dashboard
    CWM --> Dashboard
    BM --> Dashboard
    
    Dashboard --> Alerts[🚨 Alertas]:::alert
    Dashboard --> Reports[📄 Relatórios]:::report
    
    classDef user fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef aws fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef ai fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef obs fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
    classDef langsmith fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff
    classDef dash fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef alert fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    classDef report fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
```

### Métricas por Camada

| Camada | Ferramenta | Métricas | Acesso |
|--------|-----------|----------|--------|
| **CDN** | CloudFront Logs | Cache hit rate, latência edge, geo-distribuição | AWS Console |
| **API** | CloudWatch Logs | Requests/s, status codes, latência | AWS Console |
| **Compute** | CloudWatch Metrics | Invocações, duração, memória, erros | AWS Console |
| **LLM** | LangSmith | Tokens, custo, prompts, traces | https://smith.langchain.com |
| **AI** | Bedrock Metrics | Model invocations, throttling | AWS Console |

### LangSmith (Análise LLM)

```mermaid
graph LR
    Request[📨 Request]:::req --> Trace[🔍 Trace]:::trace
    
    Trace --> T1[⏱️ Latência<br/>2.3s]:::metric
    Trace --> T2[🔢 Tokens<br/>10k in / 500 out]:::metric
    Trace --> T3[💰 Custo<br/>$0.0375]:::metric
    Trace --> T4[📝 Prompt<br/>Completo]:::metric
    
    classDef req fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef trace fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff
    classDef metric fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```

**Exemplo de trace público:** https://smith.langchain.com/public/187fd186-e39b-433c-bf9c-1c5fa15a9968/r

### CloudWatch Dashboard

**Métricas principais:**
- Lambda invocations (count)
- Lambda duration (ms)
- Lambda errors (count)
- API Gateway 4xx/5xx (count)
- Bedrock throttling (count)

**Comandos:**
```bash
# Ver logs Lambda
aws logs tail /aws/lambda/juscrash-agent-core --follow

# Métricas Lambda
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=juscrash-agent-core
```

### Alertas Configurados

| Alerta | Condição | Ação |
|--------|----------|------|
| Lambda Errors | > 5 erros/min | SNS → Email |
| API Latency | > 5s p99 | SNS → Email |
| Bedrock Throttling | > 10/min | SNS → Email |
| CloudFront 5xx | > 1% requests | SNS → Email |

---

## 🎨 10. LangFlow Editor (Ambiente Local)

Workflow visual drag-and-drop:

```mermaid
graph TB
    subgraph LangFlow["🎨 LangFlow Editor Visual"]
        Input[📥 Input Node<br/>Processo JSON]:::inputStyle
        Policy[📜 Policy Node<br/>POL-1 a POL-8]:::policyStyle
        LLM[🧠 LLM Node<br/>Claude 3.5]:::llmStyle
        Output[📤 Output Node<br/>Decision JSON]:::outputStyle
        
        Input --> Policy
        Policy --> LLM
        LLM --> Output
    end
    
    LangFlow -.->|Export| JSON[📄 workflow.json]:::jsonStyle
    JSON -.->|Sync Agent| Git[📦 Git Repo]:::gitStyle
    Git -.->|Import| Backend[⚙️ Backend]:::backendStyle
    
    classDef inputStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef policyStyle fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef llmStyle fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef outputStyle fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef jsonStyle fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef gitStyle fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
    classDef backendStyle fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
```

**Vantagens:**
- ✅ Editor drag-and-drop
- ✅ Modificação sem código
- ✅ Exportação automática para JSON
- ✅ Versionamento via Git
- ✅ Rollback facilitado

**Acesso:** http://localhost:7860

---

## 🔐 11. Segurança e Compliance

Camadas de segurança implementadas:

```mermaid
graph TD
    User[👤 Usuário]:::userStyle --> HTTPS[🔒 HTTPS/TLS<br/>CloudFront]:::secStyle
    HTTPS --> WAF[🛡️ WAF<br/>Rate Limiting]:::secStyle
    WAF --> Auth[🔑 API Key<br/>Authentication]:::secStyle
    Auth --> IAM[👮 IAM Roles<br/>Lambda]:::awsStyle
    IAM --> Bedrock[🧠 Bedrock<br/>VPC Endpoint]:::awsStyle
    
    Bedrock --> Encrypt[🔐 Encryption<br/>At Rest]:::secStyle
    IAM --> Logs[📝 CloudWatch<br/>Audit Logs]:::awsStyle
    
    classDef userStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef secStyle fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    classDef awsStyle fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
```

**Compliance:**
- ✅ HTTPS obrigatório
- ✅ Rate limiting (1000 req/min)
- ✅ IAM roles com least privilege
- ✅ Encryption at rest (S3, Lambda)
- ✅ Audit logs (CloudWatch)
- ✅ VPC endpoints (Bedrock)

---

## 📈 12. Escalabilidade

Capacidade de escala automática:

```mermaid
graph LR
    Load[📊 Carga]:::loadStyle --> Scale{Escala?}:::scaleStyle
    
    Scale -->|Baixa<br/>0-100 req/s| Small[⚡ Lambda<br/>1 instância]:::smallStyle
    Scale -->|Média<br/>100-1k req/s| Medium[⚡⚡ Lambda<br/>10 instâncias]:::medStyle
    Scale -->|Alta<br/>1k-10k req/s| Large[⚡⚡⚡ Lambda<br/>100 instâncias]:::largeStyle
    
    Small --> Cost1[💰 $5/mês]:::costStyle
    Medium --> Cost2[💰 $50/mês]:::costStyle
    Large --> Cost3[💰 $500/mês]:::costStyle
    
    classDef loadStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef scaleStyle fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef smallStyle fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef medStyle fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef largeStyle fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    classDef costStyle fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

**Limites:**
- **Lambda:** 1000 concurrent executions
- **API Gateway:** 10.000 requests/second
- **Bedrock:** 100 requests/second (ajustável)
- **CloudFront:** Ilimitado

---

## 📚 Referências

- **Código:** [https://github.com/jcleitonss/JusCash_IA)
- **API Produção:** https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod
- **Frontend:** https://d26fvod1jq9hfb.cloudfront.net
- **LangSmith:** https://smith.langchain.com
- **Documentação:** [README.md](../README.md)

---

**Autor:** José Cleiton  
  
**Versão:** 1.0
