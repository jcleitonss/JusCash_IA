# 🔧 Correções do Sync Bidirecional

## 🐛 Bugs Corrigidos

### ✅ Bug 1: Comparação de Hash Incorreta (HIGH)
**Antes:**
```python
json_content = json.dumps(flow_data, indent=2)  # Apenas campo 'data'
if get_file_hash(existing) == get_file_hash(json_content):
    continue  # ❌ Nunca detectava mudanças
```

**Depois:**
```python
flow_complete = {
    "id": flow_id,
    "name": flow_name,
    "data": flow_data,
    "updated_at": updated_at.isoformat()
}
json_content = json.dumps(flow_complete, indent=2)

# Compara por timestamp primeiro
if existing_updated == flow_complete["updated_at"]:
    needs_update = False
```

### ✅ Bug 2: Query SQL Incompleta (MEDIUM)
**Antes:**
```sql
SELECT id, name, data, is_component, webhook, mcp_enabled, locked, description 
FROM flow
```

**Depois:**
```sql
SELECT id, name, data, is_component, webhook, mcp_enabled, locked, description, updated_at 
FROM flow
```

### ✅ Bug 3: Renomeação Interrompe Sync (MEDIUM)
**Antes:**
```python
if old_filename and old_filename != new_filename:
    old_path.rename(new_path)
    continue  # ❌ Não verifica conteúdo
```

**Depois:**
```python
if old_filename and old_filename != new_filename:
    old_path.rename(output_path)
    # ✅ Continua para verificar conteúdo
```

### ✅ Bug 4: Serialização Inconsistente (LOW)
**Antes:**
```python
json_content = json.dumps(flow_data, indent=2)  # Só campo 'data'
```

**Depois:**
```python
flow_complete = {
    "id": flow_id,
    "name": flow_name,
    "description": description,
    "data": flow_data,
    "updated_at": updated_at.isoformat()
}
json_content = json.dumps(flow_complete, indent=2)
```

## 🧪 Como Testar

### 1. Verificar estrutura do PostgreSQL
```bash
cd app-local
docker cp sync-agent/debug_postgres.sql langflow-postgres:/tmp/
docker exec -it langflow-postgres psql -U langflow -d langflow -f /tmp/debug_postgres.sql
```

### 2. Reiniciar sync-agent
```bash
docker-compose restart sync-agent
```

### 3. Ver logs
```bash
docker logs -f juscrash-sync-agent
```

### 4. Testar mudança no LangFlow
1. Abra http://localhost:7860
2. Edite um prompt no flow
3. Salve (Ctrl+S)
4. Aguarde 60s (intervalo do sync)
5. Verifique se o JSON foi atualizado:
```bash
cat langflow-flows/juscash_flow.json | grep "updated_at"
```

## 📊 Formato do JSON Exportado

**Antes (bugado):**
```json
{
  "nodes": [...],
  "edges": [...]
}
```

**Depois (correto):**
```json
{
  "id": "uuid-do-flow",
  "name": "JusCash Flow",
  "description": "Descrição do flow",
  "data": {
    "nodes": [...],
    "edges": [...]
  },
  "is_component": false,
  "webhook": false,
  "mcp_enabled": true,
  "locked": false,
  "updated_at": "2024-01-20T15:30:45.123456"
}
```

## 🎯 Resultado Esperado

Agora quando você editar um prompt no LangFlow:

1. ✅ PostgreSQL atualiza `updated_at`
2. ✅ Sync detecta mudança por timestamp
3. ✅ JSON é atualizado com novo conteúdo
4. ✅ Log mostra: `⬇️ juscash_flow.json (atualizado)`

## 🔍 Debug

Se ainda não funcionar, verifique:

```bash
# 1. Ver se updated_at está sendo atualizado no banco
docker exec -it langflow-postgres psql -U langflow -d langflow -c \
  "SELECT name, updated_at FROM flow ORDER BY updated_at DESC LIMIT 5;"

# 2. Ver logs detalhados do sync
docker logs juscrash-sync-agent --tail 50

# 3. Forçar export manual
docker exec -it juscrash-sync-agent python -c "
from sync_bidirectional import export_flows
export_flows()
"
```
