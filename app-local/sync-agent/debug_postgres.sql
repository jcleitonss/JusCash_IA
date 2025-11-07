-- Query para verificar estrutura da tabela flow
SELECT 
    id,
    name,
    description,
    data,
    is_component,
    webhook,
    mcp_enabled,
    locked,
    created_at,
    updated_at,
    user_id
FROM flow 
WHERE user_id IS NOT NULL
LIMIT 1;

-- Query para ver apenas metadados (sem campo data que é grande)
SELECT 
    id,
    name,
    description,
    is_component,
    webhook,
    mcp_enabled,
    locked,
    created_at,
    updated_at
FROM flow 
WHERE user_id IS NOT NULL;
