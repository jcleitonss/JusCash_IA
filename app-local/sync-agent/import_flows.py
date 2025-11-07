"""
Importa JSONs para PostgreSQL com todos os campos obrigatórios
"""
import psycopg2
import json
from pathlib import Path
import os

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "langflow-db"),
    "database": os.getenv("POSTGRES_DB", "langflow"),
    "user": os.getenv("POSTGRES_USER", "langflow"),
    "password": os.getenv("POSTGRES_PASSWORD", "langflow")
}

USER_ID = "71df9683-df17-4702-a302-c661862c55e9"
FOLDER_ID = "ae7ae4a4-d2c1-4396-a9bb-bece918a9f1d"

def import_flows():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    for json_file in Path("/app/langflow-flows").glob("*.json"):
        flow_name = json_file.stem
        flow_data = json.loads(json_file.read_text(encoding="utf-8"))
        
        cur.execute('''
            INSERT INTO flow (
                name, user_id, folder_id, data, 
                is_component, webhook, mcp_enabled, locked,
                access_type, updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (name, user_id) DO UPDATE SET
                data = EXCLUDED.data,
                is_component = EXCLUDED.is_component,
                webhook = EXCLUDED.webhook,
                mcp_enabled = EXCLUDED.mcp_enabled,
                locked = EXCLUDED.locked,
                updated_at = NOW()
        ''', (
            flow_name,
            USER_ID,
            FOLDER_ID if flow_name != "jus" else None,
            json.dumps(flow_data),
            False,
            False,
            False,
            False,
            'PRIVATE'
        ))
        
        print(f"✅ {flow_name}")
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    import_flows()
