# 📊 JUSCRASH - Diagramas Técnicos

Coleção completa de diagramas Mermaid para copiar e colar em documentações.

---

## 🎯 Fluxo Simplificado (3 Passos)

```mermaid
graph LR
    A[📄 Processo]:::input --> B[🧠 IA Claude 3.5]:::ai
    B --> C{Decisão}:::decision
    C -->|✅| D[APROVADO]:::approved
    C -->|❌| E[REJEITADO]:::rejected
    C -->|⚠️| F[INCOMPLETO]:::incomplete
    
    classDef input fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    classDef ai fill:#10B981,stroke:#059669,stroke-width:4px,color:#fff
    classDef decision fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff
    classDef approved fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
    classDef rejected fill:#EF4444,stroke:#DC2626,stroke-width:3px,color:#fff
    classDef incomplete fill:#F59E0B,stroke:#D97706,stroke-width:3px,color:#fff
```

---

## 🏗️ Arquitetura AWS Completa

```mermaid
graph TB
    User[👤 Usuário]:::userStyle --> CF[☁️ CloudFront CDN]:::awsStyle
    CF --> S3[📦 S3 Bucket<br/>Frontend React]:::awsStyle
    S3 --> API[🚪 API Gateway]:::awsStyle
    API --> Lambda[⚡ Lambda Function]:::awsStyle
    Lambda --> LG[🔄 LangGraph]:::langStyle
    LG --> Bedrock[🧠 AWS Bedrock<br/>Claude 3.5]:::aiStyle
    
    Lambda -.-> LS[📊 LangSmith]:::obsStyle
    Lambda -.-> CW[📈 CloudWatch]:::awsStyle
    
    classDef userStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    classDef awsStyle fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef langStyle fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef aiStyle fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
    classDef obsStyle fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

---

## 🔄 Sequência de Análise

```mermaid
sequenceDiagram
    participant U as 👤 Usuário
    participant F as 🖥️ Frontend
    participant A as 🚪 API Gateway
    participant L as ⚡ Lambda
    participant W as 🔄 LangGraph
    participant B as 🧠 Bedrock
    participant O as 📊 LangSmith

    U->>F: Upload processo.json
    F->>A: POST /api/v1/verificar
    A->>L: Invoke Lambda
    L->>W: Inicia workflow
    
    rect rgb(124, 58, 237, 0.1)
        Note over W,B: Análise LLM
        W->>W: Monta prompt + POL-1 a POL-8
        W->>B: Invoke Claude 3.5
        B->>B: Analisa 200k tokens
        B-->>W: JSON estruturado
    end
    
    W->>W: Valida resposta
    W-->>L: Decision + Rationale
    L->>O: Registra trace
    L-->>A: Response JSON
    A-->>F: 200 OK
    F-->>U: ✅ Decisão exibida
```

---

## 🎯 Árvore de Políticas

```mermaid
graph TD
    Start([📄 Processo]):::start --> POL1{POL-1<br/>Transitado?}
    
    POL1 -->|❌| INC1[⚠️ INCOMPLETE]:::inc
    POL1 -->|✅| POL2{POL-2<br/>Valor?}
    
    POL2 -->|❌| INC2[⚠️ INCOMPLETE]:::inc
    POL2 -->|✅| POL3{POL-3<br/>≥ R$ 1k?}
    
    POL3 -->|❌| REJ1[❌ REJECTED]:::rej
    POL3 -->|✅| POL4{POL-4<br/>Trabalhista?}
    
    POL4 -->|✅| REJ2[❌ REJECTED]:::rej
    POL4 -->|❌| POL5{POL-5<br/>Óbito?}
    
    POL5 -->|✅| REJ3[❌ REJECTED]:::rej
    POL5 -->|❌| POL6{POL-6<br/>Substab?}
    
    POL6 -->|✅| REJ4[❌ REJECTED]:::rej
    POL6 -->|❌| POL7{POL-7<br/>Honorários?}
    
    POL7 -->|❌| INC3[⚠️ INCOMPLETE]:::inc
    POL7 -->|✅| POL8{POL-8<br/>Docs OK?}
    
    POL8 -->|❌| INC4[⚠️ INCOMPLETE]:::inc
    POL8 -->|✅| APR[✅ APPROVED]:::app
    
    classDef start fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    classDef app fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
    classDef rej fill:#EF4444,stroke:#DC2626,stroke-width:3px,color:#fff
    classDef inc fill:#F59E0B,stroke:#D97706,stroke-width:3px,color:#fff
```

---

## 🐳 Docker Compose Local

```mermaid
graph LR
    subgraph Docker["🐳 Docker Compose"]
        LF[🎨 LangFlow<br/>:7860]:::langflow
        BE[⚙️ Backend<br/>:8000]:::backend
        FE[🖥️ Frontend<br/>:5173]:::frontend
        SA[🔄 Sync Agent]:::sync
    end
    
    User[👤 Dev]:::user --> FE
    User --> LF
    FE --> BE
    LF -.-> SA
    SA -.-> Git[(📦 Git)]:::git
    BE --> Bedrock[🧠 Bedrock]:::ai
    
    classDef user fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef langflow fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef backend fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef frontend fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef sync fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef git fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
    classDef ai fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
```

---

## 🚀 Pipeline Deploy

```mermaid
graph LR
    Dev[👨💻 Dev]:::dev --> Git[📦 Git]:::git
    Git --> TF[🏗️ Terraform]:::tf
    
    TF --> Lambda[⚡ Lambda]:::aws
    TF --> S3[📦 S3]:::aws
    TF --> API[🚪 API GW]:::aws
    TF --> CF[☁️ CloudFront]:::aws
    
    Lambda --> Prod[🚀 Prod]:::prod
    S3 --> Prod
    API --> Prod
    CF --> Prod
    
    Prod --> Mon[📊 Monitor]:::mon
    Mon --> LS[LangSmith]:::obs
    Mon --> CW[CloudWatch]:::obs
    
    classDef dev fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef git fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
    classDef tf fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef aws fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef prod fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
    classDef mon fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef obs fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

---

## 💰 Breakdown de Custos

```mermaid
pie title Custo Mensal (~$26 para 10k requests)
    "Bedrock Claude 3.5" : 15.00
    "Lambda Compute" : 5.00
    "CloudFront CDN" : 5.00
    "API Gateway" : 0.35
    "S3 Storage" : 0.50
    "ECR Registry" : 0.05
```

---

## 🔍 Workflow LangGraph

```mermaid
stateDiagram-v2
    [*] --> Receive: Processo JSON
    
    Receive --> Validate: Validação
    Validate --> Check: Políticas
    
    Check --> Analyze: Análise LLM
    
    state Analyze {
        [*] --> Prompt
        Prompt --> Invoke
        Invoke --> Parse
        Parse --> Validate2
        Validate2 --> [*]
    }
    
    Analyze --> Decision
    
    state Decision {
        [*] --> choice
        choice --> Approved: ✅
        choice --> Rejected: ❌
        choice --> Incomplete: ⚠️
    }
    
    Decision --> Log: Trace
    Log --> [*]
```

---

## 📊 Tokens LLM

```mermaid
graph LR
    Input[📥 Input]:::input --> Prompt[System<br/>~2k tokens]:::prompt
    Input --> Process[Processo<br/>~3k tokens]:::process
    Input --> Docs[Docs<br/>~5k tokens]:::docs
    
    Prompt --> Total[Total<br/>~10k tokens]:::total
    Process --> Total
    Docs --> Total
    
    Total --> LLM[🧠 Claude 3.5]:::llm
    
    LLM --> Output[📤 Output<br/>~500 tokens]:::output
    
    classDef input fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef prompt fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef process fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef docs fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef total fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef llm fill:#FF9900,stroke:#CC7A00,stroke-width:3px,color:#fff
    classDef output fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

---

## 🎨 LangFlow Editor

```mermaid
graph TB
    subgraph LangFlow["🎨 LangFlow Editor"]
        Input[📥 Input<br/>Processo]:::input
        Policy[📜 Policy<br/>POL-1 a 8]:::policy
        LLM[🧠 LLM<br/>Claude 3.5]:::llm
        Output[📤 Output<br/>Decision]:::output
        
        Input --> Policy
        Policy --> LLM
        LLM --> Output
    end
    
    LangFlow -.->|Export| JSON[📄 JSON]:::json
    JSON -.->|Sync| Git[📦 Git]:::git
    Git -.->|Import| Backend[⚙️ Backend]:::backend
    
    classDef input fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef policy fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef llm fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef output fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef json fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef git fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
    classDef backend fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
```

---

## 🔐 Segurança

```mermaid
graph TD
    User[👤 Usuário]:::user --> HTTPS[🔒 HTTPS/TLS]:::sec
    HTTPS --> WAF[🛡️ WAF]:::sec
    WAF --> Auth[🔑 Auth]:::sec
    Auth --> IAM[👮 IAM]:::aws
    IAM --> Bedrock[🧠 Bedrock]:::aws
    
    Bedrock --> Encrypt[🔐 Encryption]:::sec
    IAM --> Logs[📝 Audit Logs]:::aws
    
    classDef user fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef sec fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    classDef aws fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
```

---

## 📈 Escalabilidade

```mermaid
graph LR
    Load[📊 Carga]:::load --> Scale{Escala?}:::scale
    
    Scale -->|0-100| Small[⚡ 1 inst]:::small
    Scale -->|100-1k| Medium[⚡⚡ 10 inst]:::med
    Scale -->|1k-10k| Large[⚡⚡⚡ 100 inst]:::large
    
    Small --> Cost1[💰 $5/mês]:::cost
    Medium --> Cost2[💰 $50/mês]:::cost
    Large --> Cost3[💰 $500/mês]:::cost
    
    classDef load fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef scale fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef small fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef med fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef large fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    classDef cost fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

---

## 🎯 Mindmap Políticas

```mermaid
mindmap
  root((🏛️<br/>JUSCRASH))
    ✅ Elegibilidade
      POL-1: Transitado
      POL-2: Valor informado
    ❌ Rejeição
      POL-3: Valor mínimo
      POL-4: Trabalhista
      POL-5: Óbito
      POL-6: Substabelecimento
    📋 Documentação
      POL-7: Honorários
      POL-8: Docs completos
```

---

## 📅 Timeline Roadmap

```mermaid
timeline
    title Evolução JUSCRASH
    section Q1 2025
        MVP : Análise básica
            : 8 políticas
            : Claude 3.5
    section Q2 2025
        Expansão : OCR docs
                 : Multi-tribunal
                 : API pública
    section Q3 2025
        IA Avançada : Fine-tuning
                    : Predição
                    : Análise risco
    section Q4 2025
        Enterprise : Multi-tenant
                   : Analytics
                   : Mobile app
```

---

## 🏆 Comparação

```mermaid
graph TD
    subgraph Tradicional["❌ Tradicional"]
        T1[Manual]:::trad
        T2[Excel]:::trad
        T3[Dias]:::trad
        T4[Erros]:::trad
    end
    
    subgraph JUSCRASH["✅ JUSCRASH"]
        J1[IA Auto]:::jus
        J2[Web]:::jus
        J3[3s]:::jus
        J4[95%+]:::jus
    end
    
    classDef trad fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    classDef jus fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```

---

## 💡 Stack Tech

```mermaid
graph TB
    subgraph Frontend["🖥️ Frontend"]
        React[React 18]:::fe
        MUI[Material UI]:::fe
    end
    
    subgraph Backend["⚙️ Backend"]
        FastAPI[FastAPI]:::be
        LangGraph[LangGraph]:::be
    end
    
    subgraph AI["🧠 IA"]
        Bedrock[Bedrock]:::ai
        Claude[Claude 3.5]:::ai
    end
    
    subgraph Infra["☁️ Infra"]
        Lambda[Lambda]:::infra
        Terraform[Terraform]:::infra
    end
    
    Frontend --> Backend
    Backend --> AI
    AI --> Infra
    
    classDef fe fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef be fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef ai fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef infra fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
```

---

## 📊 Observabilidade

```mermaid
graph TD
    Request[📨 Request]:::req --> Trace[🔍 Trace]:::trace
    
    Trace --> Latency[⏱️ Latência]:::metric
    Trace --> Tokens[🔢 Tokens]:::metric
    Trace --> Cost[💰 Custo]:::metric
    Trace --> Prompts[📝 Prompts]:::metric
    Trace --> Errors[❌ Erros]:::metric
    
    Latency --> Dashboard[📊 Dashboard]:::dash
    Tokens --> Dashboard
    Cost --> Dashboard
    Prompts --> Dashboard
    Errors --> Dashboard
    
    Dashboard --> Insights[💡 Insights]:::insight
    
    classDef req fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef trace fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff
    classDef metric fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef dash fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef insight fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
```

---

## 🎯 ROI

```mermaid
graph LR
    subgraph Antes["❌ Antes"]
        A1[👤 3 analistas]:::before
        A2[💰 R$ 15k/mês]:::before
        A3[⏱️ 2h/processo]:::before
    end
    
    subgraph Depois["✅ JUSCRASH"]
        D1[🤖 Automático]:::after
        D2[💰 R$ 26/mês]:::after
        D3[⏱️ 3s/processo]:::after
    end
    
    Antes -.-> Economia[💵 99.8%<br/>economia]:::roi
    Antes -.-> Velocidade[⚡ 2400x<br/>rápido]:::roi
    
    classDef before fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    classDef after fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef roi fill:#F59E0B,stroke:#D97706,stroke-width:3px,color:#fff
```

---

## 📝 Como Usar

1. Copie o código Mermaid desejado
2. Cole no seu README.md ou documentação
3. O diagrama renderiza automaticamente no GitHub/GitLab
4. Personalize cores e textos conforme necessário

**Compatível com:**
- ✅ GitHub
- ✅ GitLab
- ✅ VS Code (extensão Mermaid)
- ✅ Notion
- ✅ Confluence
- ✅ Markdown Preview Enhanced

---

**Autor:** José Cleiton  
**Projeto:** JUSCRASH  
**Data:** Janeiro 2025
