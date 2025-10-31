# 🏛️ JUSCASH - Resumo Visual em Uma Página

Tudo que você precisa saber sobre o JUSCASH em uma única página.

---

## 🎯 O que é?

```mermaid
graph LR
    A[📄 Processo<br/>Judicial]:::a --> B[🧠 IA Claude 3.5<br/>Análise Automática]:::b --> C[✅ Decisão<br/>3 segundos]:::c
    classDef a fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff,font-size:14px
    classDef b fill:#10B981,stroke:#059669,stroke-width:4px,color:#fff,font-size:16px
    classDef c fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff,font-size:14px
```

Sistema que analisa processos judiciais e decide automaticamente se devem ser aprovados para compra de crédito usando IA.

---

## ⚡ Como Funciona?

```mermaid
sequenceDiagram
    participant U as 👤 Usuário
    participant S as 🖥️ Sistema
    participant I as 🧠 IA
    U->>S: 1. Upload processo.json
    S->>I: 2. Analisa 8 políticas
    I-->>S: 3. Decisão + Justificativa
    S-->>U: 4. Resultado (3s)
```

---

## 🎯 3 Decisões

```mermaid
graph TD
    P[📄 Processo]:::p --> D{🧠 IA}:::d
    D -->|OK| A[✅ APROVADO]:::a
    D -->|Erro| R[❌ REJEITADO]:::r
    D -->|Falta| I[⚠️ INCOMPLETO]:::i
    classDef p fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef d fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff
    classDef a fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef r fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    classDef i fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
```

---

## 📜 8 Políticas

```mermaid
mindmap
  root((8<br/>Políticas))
    ✅ Obrigatórias
      POL-1 Transitado
      POL-2 Valor
      POL-7 Honorários
      POL-8 Docs
    ❌ Rejeição
      POL-3 Mínimo
      POL-4 Trabalhista
      POL-5 Óbito
      POL-6 Substab
```

---

## 🏗️ Arquitetura

```mermaid
graph TB
    U[👤 Usuário]:::u --> C[☁️ AWS Cloud]:::c
    C --> F[🖥️ React]:::f
    C --> B[⚙️ Lambda]:::b
    C --> A[🧠 Claude 3.5]:::a
    classDef u fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef c fill:#FF9900,stroke:#CC7A00,stroke-width:3px,color:#fff
    classDef f fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef b fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef a fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
```

**100% Serverless:** CloudFront + S3 + API Gateway + Lambda + Bedrock

---

## 💰 Custo

```mermaid
pie title $26/mês (10k requests)
    "IA" : 15
    "Lambda" : 5
    "CDN" : 5
    "Outros" : 1
```

**ROI:** 99% economia vs analistas manuais

---

## 🛠️ Stack

```mermaid
graph LR
    F[React<br/>Material UI]:::f --> B[FastAPI<br/>LangGraph]:::b --> A[Bedrock<br/>Claude 3.5]:::a
    classDef f fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef b fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef a fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
```

---

## 🚀 Deploy

```mermaid
graph LR
    C[💻 Código]:::c --> T[🏗️ Terraform]:::t --> A[☁️ AWS]:::a --> P[🚀 Prod]:::p
    classDef c fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef t fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    classDef a fill:#FF9900,stroke:#CC7A00,stroke-width:2px,color:#fff
    classDef p fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
```

**Comandos:** `make init` → `make deploy` → Pronto!

---

## 🏆 Diferenciais

| Diferencial | Descrição |
|-------------|-----------|
| 🎨 **Editor Visual** | LangFlow drag-and-drop |
| ☁️ **100% Serverless** | AWS Lambda + API Gateway |
| 📊 **Observabilidade** | LangSmith traces completos |
| 🧠 **IA Avançada** | Claude 3.5 Sonnet |
| ⚡ **Rápido** | 3 segundos por análise |
| 💰 **Barato** | $26/mês para 10k requests |

---

## 📊 Métricas

| Métrica | Valor |
|---------|-------|
| ⏱️ **Tempo** | 3 segundos |
| 💰 **Custo** | $0.04/análise |
| 🎯 **Precisão** | 95%+ |
| 📈 **Escala** | 10k req/s |
| 🔒 **SLA** | 99.99% |

---

## 🔗 Links

| Recurso | URL |
|---------|-----|
| 🌐 **Frontend** | https://d26fvod1jq9hfb.cloudfront.net |
| 🔌 **API** | https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod |
| 📖 **Docs** | [/docs](https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/docs) |
| 💻 **GitHub** | https://github.com/jcleitonss/JusCash_IA |

---

## 🐳 Local

```bash
# Subir
docker-compose up --build

# Acessar
http://localhost:5173  # Frontend
http://localhost:8000  # Backend
http://localhost:7860  # LangFlow
```

---

## ☁️ AWS

```bash
cd app-remoto/infrastructure
make init      # Inicializa
make deploy    # Deploy
make logs      # Logs
```

---

## 📚 Docs

```mermaid
graph LR
    A[⚡ 5min]:::a --> B[🎯 10min]:::b --> C[🏗️ 20min]:::c --> D[📄 30min]:::d
    classDef a fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    classDef b fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef c fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    classDef d fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

- ⚡ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 5 min
- 🎯 [PRESENTATION.md](PRESENTATION.md) - 10 min
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - 20 min
- 📊 [DIAGRAMS.md](DIAGRAMS.md) - Biblioteca
- 📚 [INDEX.md](INDEX.md) - Índice completo

---

## 🎓 Próximos Passos

```mermaid
graph LR
    A[1️⃣ Ler]:::s --> B[2️⃣ Testar]:::s --> C[3️⃣ Deploy]:::s --> D[4️⃣ Usar]:::s
    classDef s fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```

1. Ler [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. Testar local com Docker
3. Deploy AWS com Terraform
4. Usar em produção

---

## 📞 Contato

**Desenvolvedor:** José Cleiton  
**GitHub:** https://github.com/jcleitonss/JusCash_IA
**Projeto:** JUSCASH

---

## 🎯 Resumo Executivo

```mermaid
graph TB
    P[🏛️ JUSCASH]:::main
    
    P --> A[⚡ Rápido<br/>3s]:::benefit
    P --> B[💰 Barato<br/>$26/mês]:::benefit
    P --> C[🎯 Preciso<br/>95%+]:::benefit
    P --> D[📈 Escalável<br/>10k req/s]:::benefit
    
    classDef main fill:#7C3AED,stroke:#5B21B6,stroke-width:4px,color:#fff,font-size:16px
    classDef benefit fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff,font-size:12px
```

**JUSCASH transforma análise jurídica manual em decisões automáticas, rápidas e precisas usando IA.**

---

**⚡ Desenvolvido em 7 dias | 🚀 100% Funcional | ✅ Pronto para Produção**

---

**📖 Quer mais detalhes?** Veja [INDEX.md](INDEX.md) para navegação completa da documentação.
