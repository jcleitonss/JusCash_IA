# 🔄 JUSCRASH - Fluxo de Sincronização

Documentação visual do **Sync Agent** para sincronização bidirecional LangFlow ⇄ Git.

---

## 🎯 Visão Geral

```mermaid
graph TB
    LF[🎨 LangFlow<br/>Editor Visual]:::langflow
    PG[(🗄️ PostgreSQL<br/>LangFlow DB)]:::db
    SA[🔄 Sync Agent<br/>Bidirecional]:::sync
    FS[(💾 langflow-flows/<br/>workflow.json)]:::fs
    Git[(📦 Git Repo)]:::git
    
    LF <-->|CRUD| PG
    SA <-->|Monitora| PG
    SA <-->|Export/Import| FS
    SA -.->|Commit| Git
    
    classDef langflow fill:#7C3AED,stroke:#5B21B6,stroke-width:3px,color:#fff
    classDef db fill:#6366F1,stroke:#4338CA,stroke-width:2px,color:#fff
    classDef sync fill:#F59E0B,stroke:#D97706,stroke-width:3px,color:#fff
    classDef fs fill:#8B5CF6,stroke:#6D28D9,stroke-width:2px,color:#fff
    classDef git fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

**Componentes:**
- **LangFlow:** Editor visual drag-and-drop
- **PostgreSQL:** Banco de dados do LangFlow
- **Sync Agent:** Sincronização bidirecional (60s interval)
- **Filesystem:** Pasta `langflow-flows/` versionada
- **Git:** Repositório remoto (commits automáticos)

---

## 🔄 Fluxo Bidirecional

### 1. LangFlow → Filesystem (Export)

```mermaid
sequenceDiagram
    participant D as 👨💻 Dev
    participant L as 🎨 LangFlow
    participant P as 🗄️ PostgreSQL
    participant S as 🔄 Sync Agent
    participant F as 💾 Filesystem
    participant G as 📦 Git

    rect rgb(124, 58, 237, 0.1)
        Note over D,P: Edição no LangFlow
        D->>L: 1. Edita workflow (drag-and-drop)
        L->>P: 2. Salva no PostgreSQL
        P-->>L: 3. Confirma (updated_at)
    end
    
    rect rgb(245, 158, 11, 0.1)
        Note over S,F: Export Automático (60s)
        S->>P: 4. SELECT * FROM flow
        P-->>S: 5. Retorna flows
        S->>S: 6. Calcula hash SHA256
        
        alt Flow modificado
            S->>F: 7. Exporta workflow.json
            F-->>S: 8. Salvo
        end
    end
    
    rect rgb(107, 114, 128, 0.1)
        Note over S,G: Commit Automático
        S->>G: 9. git add workflow.json
        S->>G: 10. git commit -m "sync: workflow"
        S->>G: 11. git push origin dev
    end
```

**Intervalo:** 60 segundos  
**Tracking:** Por `updated_at` do PostgreSQL  
**Hash:** SHA256 para detectar mudanças

---

### 2. Filesystem → LangFlow (Import)

```mermaid
sequenceDiagram
    participant D as 👨💻 Dev
    participant G as 📦 Git
    participant F as 💾 Filesystem
    participant S as 🔄 Sync Agent
    participant P as 🗄️ PostgreSQL
    participant L as 🎨 LangFlow

    rect rgb(107, 114, 128, 0.1)
        Note over D,F: Adicionar workflow.json
        D->>G: 1. git add workflow.json
        D->>G: 2. git commit
        D->>G: 3. git push
        G->>F: 4. Pull no container
    end
    
    rect rgb(245, 158, 11, 0.1)
        Note over S,P: Import Automático
        S->>F: 5. Detecta workflow.json novo
        S->>S: 6. Valida JSON
        S->>P: 7. SELECT id FROM flow WHERE name=?
        
        alt Flow não existe
            S->>P: 8. INSERT INTO flow
            P-->>S: 9. Retorna flow_id
        end
    end
    
    rect rgb(124, 58, 237, 0.1)
        Note over S,L: Ativação na UI
        S->>L: 10. Acessa /flow/{id}
        L->>L: 11. Carrega workflow
        L-->>D: 12. Workflow disponível ✅
    end
```

**Sentinela:** Arquivo `.initialized` (primeira vez)  
**Validação:** Schema JSON + campos obrigatórios  
**Ativação:** Playwright abre URL do flow

---

## 📦 Estrutura de Dados

### workflow.json (Exportado)

```json
{
  "id": "uuid-do-flow",
  "name": "workflow",
  "description": "Workflow principal",
  "data": {
    "nodes": [...],
    "edges": [...]
  },
  "is_component": false,
  "webhook": false,
  "mcp_enabled": true,
  "locked": false,
  "updated_at": "2025-01-20T10:30:00"
}
```

### id_mapping.json (Tracking)

```json
{
  "uuid-flow-1": "workflow",
  "uuid-flow-2": "juscash_flow"
}
```

**Função:** Mapeia IDs do PostgreSQL → nomes de arquivo

---

## 🔧 Configuração

### Variáveis de Ambiente

**Arquivo:** `keys/.env`

```bash
# PostgreSQL
POSTGRES_URL=postgresql://langflow:langflow@postgres:5432/langflow

# Git
GITHUB_TOKEN=ghp_...
GITHUB_USER=seu-usuario
GITHUB_REPO=JusCash_IA
```

### Docker Compose

```yaml
sync-agent:
  build: ./sync-agent
  volumes:
    - ./langflow-flows:/app/langflow-flows
  networks:
    - juscrash-network
  depends_on:
    - langflow
    - postgres
  command: ["python", "-u", "sync_bidirectional.py"]
```

---

## 📊 Logs

```bash
# Ver logs do Sync Agent
docker logs -f juscrash-sync-agent

# Exemplo de saída
🔄 LangFlow Sync Bidirecional iniciado
⬇️  workflow.json (atualizado)
📝 juscash_flow.json → workflow.json
🗑️  old_flow.json (excluído)
```

---

## 🐛 Troubleshooting

| Problema | Solução |
|----------|---------|
| PostgreSQL não conecta | Verificar `POSTGRES_URL` em `keys/.env` |
| Workflow não aparece no LangFlow | Aguardar 60s ou reiniciar sync-agent |
| Git não commita | Verificar `GITHUB_TOKEN` |
| JSON inválido | Validar schema em https://jsonlint.com |

---

## 📚 Referências

- [SYNC_TRADUTOR.md](SYNC_TRADUTOR.md) - Tradução JSON → Python
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura completa
- Código: `app-local/sync-agent/sync_bidirectional.py`

---

**Autor:** José Cleiton  
**Projeto:** JUSCASH  
**Versão:** 1.0
