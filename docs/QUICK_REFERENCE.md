# ⚡ JUSCRASH - Referência Rápida Visual

Guia visual rápido para entender o JusCash em 5 minutos.

---

## 🎯 O que é?

```mermaid
graph LR
    A[📄 Processo<br/>Judicial]:::input --> B[🧠 IA<br/>Análise]:::ai --> C[✅ Decisão<br/>Automática]:::output
    
    classDef input fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff,font-size:16px
    classDef ai fill:#10B981,stroke:#059669,stroke-width:4px,color:#fff,font-size:18px
    classDef output fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff,font-size:16px
```

**Sistema que analisa processos judiciais e decide automaticamente se devem ser aprovados para compra de crédito.**

---

## ⚡ Como funciona?

```mermaid
graph LR
    Step1[1️⃣ Upload]:::s1 --> Step2[2️⃣ IA Analisa]:::s2 --> Step3[3️⃣ Decisão]:::s3
    
    classDef s1 fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff,font-size:18px
    classDef s2 fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff,font-size:18px
    classDef s3 fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff,font-size:18px
```

1. **Upload:** Usuário envia JSON do processo
2. **IA Analisa:** Claude 3.5 verifica 8 políticas
3. **Decisão:** Sistema retorna aprovado/rejeitado/incompleto

**Tempo:** 3 segundos | **Custo:** $0.04 | **Precisão:** 95%+

---

## 🎯 3 Decisões Possíveis

```mermaid
graph TD
    Process[📄 Processo]:::process --> Decision{🧠 Análise}:::decision
    
    Decision -->|Todas políticas OK| Approved[✅ APROVADO<br/>Comprar crédito]:::approved
    Decision -->|Violação de regra| Rejected[❌ REJEITADO<br/>Não comprar]:::rejected
    Decision -->|Falta documento| Incomplete[⚠️ INCOMPLETO<br/>Solicitar docs]:::incomplete
    
    classDef process fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff,font-size:14px
    classDef decision fill:#7C3AED,stroke:#5B21B6,stroke-width:4px,color:#fff,font-size:16px
    classDef approved fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff,font-size:14px
    classDef rejected fill:#EF4444,stroke:#DC2626,stroke-width:3px,color:#fff,font-size:14px
    classDef incomplete fill:#F59E0B,stroke:#D97706,stroke-width:3px,color:#fff,font-size:14px
```

---

## 📜 8 Políticas de Negócio

```mermaid
mindmap
  root((🏛️<br/>8 Políticas))
    ✅ Obrigatórias
      POL-1<br/>Transitado
      POL-2<br/>Valor
      POL-7<br/>Honorários
      POL-8<br/>Docs
    ❌ Rejeição
      POL-3<br/>Mínimo R$ 1k
      POL-4<br/>Trabalhista
      POL-5<br/>Óbito
      POL-6<br/>Substab
```

| Tipo | Políticas | Ação |
|------|-----------|------|
| ✅ **Obrigatórias** | POL-1, POL-2, POL-7, POL-8 | Se faltar → INCOMPLETO |
| ❌ **Rejeição** | POL-3, POL-4, POL-5, POL-6 | Se violar → REJEITADO |

---

## 🏗️ Arquitetura (Simplificada)

```mermaid
graph TB
    User[👤 Usuário]:::user --> Cloud[☁️ AWS Cloud]:::cloud
    
    Cloud --> Frontend[🖥️ Frontend<br/>React]:::fe
    Cloud --> Backend[⚙️ Backend<br/>Lambda]:::be
    Cloud --> AI[🧠 IA<br/>Claude 3.5]:::ai
    
    classDef user fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff,font-size:14px
    classDef cloud fill:#FF9900,stroke:#CC7A00,stroke-width:4px,color:#fff,font-size:16px
    classDef fe fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff,font-size:12px
    classDef be fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff,font-size:12px
    classDef ai fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff,font-size:12px
```

**100% Serverless AWS:**
- Frontend: CloudFront + S3
- Backend: Lambda + API Gateway
- IA: AWS Bedrock (Claude 3.5)

---

## 💰 Custo

```mermaid
pie title $26/mês para 10k requests
    "IA Claude 3.5" : 15
    "Lambda" : 5
    "CloudFront" : 5
    "Outros" : 1
```

**Comparação:**
- ❌ **Antes:** 3 analistas × R$ 5k = R$ 15.000/mês
- ✅ **Agora:** AWS Serverless = R$ 150/mês (~$26)
- 💰 **Economia:** 99% de redução

---

## 🚀 Stack Tecnológico

```mermaid
graph LR
    subgraph Frontend
        A1[React 18]:::tech
        A2[Material UI]:::tech
    end
    
    subgraph Backend
        B1[FastAPI]:::tech
        B2[LangGraph]:::tech
    end
    
    subgraph IA
        C1[AWS Bedrock]:::tech
        C2[Claude 3.5]:::tech
    end
    
    Frontend --> Backend --> IA
    
    classDef tech fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```

**Principais tecnologias:**
- 🖥️ Frontend: React + Material UI
- ⚙️ Backend: FastAPI + LangGraph
- 🧠 IA: AWS Bedrock + Claude 3.5
- ☁️ Infra: Lambda + Terraform

---

## 📊 Fluxo Completo

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant F as 🖥️ Frontend
    participant B as ⚙️ Backend
    participant A as 🧠 IA

    U->>F: 1. Upload processo
    F->>B: 2. POST /verificar
    B->>A: 3. Analisa com IA
    A-->>B: 4. Decisão
    B-->>F: 5. Response
    F-->>U: 6. Exibe resultado
    
    Note over U,A: Tempo total: ~3 segundos
```

---

## 🎯 Exemplo de Uso

### Input (JSON)
```json
{
  "numeroProcesso": "0001234-56.2023.4.05.8100",
  "classe": "Cumprimento de Sentença",
  "esfera": "Federal",
  "documentos": [
    {
      "nome": "Certidão de Trânsito em Julgado",
      "texto": "Certifico que transitou..."
    }
  ]
}
```

### Output (JSON)
```json
{
  "decision": "approved",
  "rationale": "Processo transitado (POL-1), valor R$ 67.592 informado (POL-2)...",
  "citacoes": ["POL-1", "POL-2"]
}
```

---

## 🐳 Ambiente Local

```mermaid
graph LR
    Dev[👨💻 Dev]:::dev --> Docker[🐳 Docker]:::docker
    
    Docker --> LF[LangFlow<br/>:7860]:::service
    Docker --> BE[Backend<br/>:8000]:::service
    Docker --> FE[Frontend<br/>:5173]:::service
    
    classDef dev fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef docker fill:#2496ED,stroke:#1D7FBD,stroke-width:3px,color:#fff
    classDef service fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```

**Comandos:**
```bash
# Subir tudo
docker-compose up --build

# Acessar
http://localhost:5173  # Frontend
http://localhost:8000  # Backend
http://localhost:7860  # LangFlow
```

---

## ☁️ Deploy AWS

```mermaid
graph LR
    Code[💻 Código]:::code --> TF[🏗️ Terraform]:::tf --> AWS[☁️ AWS]:::aws --> Live[🚀 Produção]:::live
    
    classDef code fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef tf fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef aws fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef live fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
```

**Comandos:**
```bash
cd app-remoto/infrastructure
make init      # Inicializa
make deploy    # Deploy completo
make logs      # Ver logs
```

---

## 🏆 Diferenciais

```mermaid
graph TD
    JusCash[🏛️ JusCash]:::main
    
    JusCash --> D1[🎨 Editor Visual<br/>LangFlow]:::diff
    JusCash --> D2[☁️ 100% Serverless<br/>AWS]:::diff
    JusCash --> D3[📊 Observabilidade<br/>LangSmith]:::diff
    JusCash --> D4[🧠 IA Avançada<br/>Claude 3.5]:::diff
    
    classDef main fill:#7C3AED,stroke:#5B21B6,stroke-width:4px,color:#fff,font-size:16px
    classDef diff fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff,font-size:12px
```

**Único com:**
- ✅ Editor visual drag-and-drop (LangFlow)
- ✅ Arquitetura serverless completa
- ✅ Observabilidade profissional (LangSmith)
- ✅ Frontend moderno (React + MUI)

---

## 📈 ROI

```mermaid
graph LR
    Before[❌ Antes<br/>R$ 15k/mês<br/>2h/processo]:::before
    After[✅ Agora<br/>R$ 150/mês<br/>3s/processo]:::after
    
    Before -.->|99% economia| ROI[💰 ROI]:::roi
    Before -.->|2400x rápido| ROI
    
    classDef before fill:#EF4444,stroke:#DC2626,stroke-width:3px,color:#fff,font-size:14px
    classDef after fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff,font-size:14px
    classDef roi fill:#F59E0B,stroke:#D97706,stroke-width:4px,color:#fff,font-size:16px
```

---

## 🔗 Links Rápidos

| Recurso | URL |
|---------|-----|
| 🌐 **Frontend** | https://d26fvod1jq9hfb.cloudfront.net |
| 🔌 **API** | https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod |
| 📖 **Docs** | [/docs](https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/docs) |
| 📊 **LangSmith** | https://smith.langchain.com |
| 💻 **GitHub** | https://github.com/jcleitonss/JusCash |

---

## 📚 Documentação Completa

```mermaid
graph TD
    Start[📖 Docs]:::start
    
    Start --> A[🏗️ Arquitetura<br/>ARCHITECTURE.md]:::doc
    Start --> B[🎯 Apresentação<br/>PRESENTATION.md]:::doc
    Start --> C[📊 Diagramas<br/>DIAGRAMS.md]:::doc
    Start --> D[⚡ Referência<br/>QUICK_REFERENCE.md]:::doc
    
    classDef start fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff
    classDef doc fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```

- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura técnica completa
- 🎯 [PRESENTATION.md](PRESENTATION.md) - Apresentação executiva
- 📊 [DIAGRAMS.md](DIAGRAMS.md) - Biblioteca de diagramas
- ⚡ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Este guia

---

## 🎓 Próximos Passos

```mermaid
graph LR
    A[1️⃣ Ler docs]:::step --> B[2️⃣ Testar local]:::step --> C[3️⃣ Deploy AWS]:::step --> D[4️⃣ Produção]:::step
    
    classDef step fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```

1. **Ler documentação:** [README.md](../README.md)
2. **Testar local:** `docker-compose up`
3. **Deploy AWS:** `make deploy`
4. **Usar em produção:** API + Frontend

---

## 📞 Contato

**Desenvolvedor:** José Cleiton  
**GitHub:** [github.com/jcleitonss/JusCash](https://github.com/jcleitonss/JusCash)  
**Projeto:** JusCash - Verificador Inteligente de Processos Judiciais

---

**⚡ Desenvolvido em 7 dias | 🚀 100% Funcional | ✅ Pronto para Produção**
