"""
Script de teste rápido do Sync Tradutor
Executa uma tradução única sem loop
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega .env local
load_dotenv()

print("🧪 Teste do Sync Tradutor")
print("=" * 60)
print(f"AWS_REGION: {os.getenv('AWS_REGION')}")
print(f"BEDROCK_MODEL_ID: {os.getenv('BEDROCK_MODEL_ID')}")
print(f"BEDROCK_AGENT_ID: {os.getenv('BEDROCK_AGENT_ID') or 'NÃO CONFIGURADO'}")
print("=" * 60)

# Importa e executa tradução
from sync_tradutor import sync_tradutor

if __name__ == "__main__":
    print("\n🚀 Executando tradução única...\n")
    success = sync_tradutor()
    
    if success:
        print("\n✅ Teste concluído com sucesso!")
    else:
        print("\n❌ Teste falhou - verifique os logs acima")
