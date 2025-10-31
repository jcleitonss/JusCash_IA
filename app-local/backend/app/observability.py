"""
Configuração de observabilidade com LangSmith
"""
import os

# Lê variáveis do ambiente (carregadas pelo Docker via .env)
LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY')
LANGSMITH_PROJECT = os.getenv('LANGSMITH_PROJECT', 'juscrash')
LANGSMITH_ENDPOINT = os.getenv('LANGSMITH_ENDPOINT', 'https://api.smith.langchain.com')
LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2', 'false')

print(f"🔍 Observability - API_KEY presente: {bool(LANGSMITH_API_KEY)}, Tracing: {LANGCHAIN_TRACING_V2}")

# Configura LangSmith se habilitado
if LANGSMITH_API_KEY and LANGCHAIN_TRACING_V2.lower() == 'true':
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
    os.environ["LANGCHAIN_ENDPOINT"] = LANGSMITH_ENDPOINT
    langsmith_enabled = True
    print(f"✅ LangSmith HABILITADO - Projeto: {LANGSMITH_PROJECT}")
else:
    langsmith_enabled = False
    print(f"⚠️ LangSmith DESABILITADO")
