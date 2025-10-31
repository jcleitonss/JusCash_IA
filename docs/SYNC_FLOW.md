# 🔄 JUSCRASH - Fluxo de Sincronização

Documentação visual do **Sync Agent** e **Sync Tradutor** para sincronização bidirecional e tradução de workflows.

---

## 🎯 Visão Geral

```mermaid
graph TB
    LF[🎨 LangFlow<br/>Editor Visual]:::langflow
    FS[(💾 langflow-flows/<br/>workflow.json)]:::fs
    SA[🔄 Sync Agent<br/>✅ Atual]:::current
    ST[🔧 Sync Tradutor<br/>🔜 Futuro]:::future
    BE[⚙️ Backend<br/>FastAPI]:::backend
    
    LF <-->|Bidirecional| SA
    SA <-->|Bidirecional| FS
    FS -.->|Identifica workflow.json| ST
    ST -.->|Gera workflow.py<br/>LangGraph| BE
    
    classDef langflow fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff
    classDef fs fill:#6B7280,stroke:#4B5563,stroke-width:3px,color:#fff
    classDef current fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
    classDef future fill:#F59E0B,stroke:#D97706,stroke-width:3px,color:#fff,stroke-dasharray: 5 5
    classDef backend fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
```

**Componentes:**
- **Sync Agent** (✅ Implementado) - Sincronização bidirecional LangFlow ⇄ Filesystem
- **Sync Tradutor** (🔜 Futuro) - Traduz workflow.json → Python LangGraph

---

## 🔄 1. Sync Agent (Atual)

### Fluxo Bidirecional

```mermaid
sequenceDiagram
    participant Dev as 👨💻 Desenvolvedor
    participant LF as 🎨 LangFlow
    participant SA as 🔄 Sync Agent
    participant FS as 💾 Filesystem
    
    rect rgb(16, 185, 129, 0.1)
        Note over SA,FS: LangFlow → Filesystem
        Dev->>LF: 1. Edita workflow (UI)
        LF->>LF: 2. Salva internamente
        
        SA->>LF: 3. GET /api/v1/flows
        LF-->>SA: 4. workflow.json
        SA->>SA: 5. Calcula hash MD5
        
        alt Modificado no LangFlow
            SA->>FS: 6. Salva workflow.json
        end
    end
    
    rect rgb(124, 58, 237, 0.1)
        Note over SA,FS: Filesystem → LangFlow
        Dev->>FS: 7. Adiciona workflow.json
        
        SA->>FS: 8. Monitora langflow-flows/
        FS-->>SA: 9. workflow.json detectado
        SA->>SA: 10. Valida JSON
        
        alt Arquivo válido
            SA->>LF: 11. POST /api/v1/flows
            LF->>LF: 12. Importa workflow
            LF-->>Dev: 13. Workflow disponível na UI ✅
        end
    end
```

---

**Autor:** José Cleiton  
**Projeto:** JUSCRASH  
**Data:** Janeiro 2025
