"""
Configuração centralizada de chaves e credenciais
"""
import os
from pathlib import Path


# Diretório base
BASE_DIR = Path(__file__).parent


def load_aws_credentials() -> tuple:
    """
    Carrega credenciais IAM da AWS do arquivo CSV
    
    Returns:
        tuple: (access_key_id, secret_access_key)
    """
    csv_path = BASE_DIR / "BedrockAPIKey-f3c8_accessKeys.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        if len(lines) < 2:
            raise ValueError("Arquivo CSV inválido")
        
        # Pega a segunda linha: Access key ID, Secret access key
        parts = lines[1].strip().split(',')
        if len(parts) < 2:
            raise ValueError("Formato CSV inválido")
        
        access_key_id = parts[0].strip()  # AKIA...
        secret_access_key = parts[1].strip()  # ...
        
        return access_key_id, secret_access_key


# ========================================
# AWS CREDENTIALS
# ========================================
AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = load_aws_credentials()
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# ========================================
# AWS BEDROCK
# ========================================
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")


# ========================================
# LANGFUSE (Observabilidade)
# ========================================
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")


# ========================================
# API
# ========================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
API_VERSION = "1.0.0"


# ========================================
# MODELOS DISPONÍVEIS
# ========================================
# Claude 3.5 Sonnet v2: anthropic.claude-3-5-sonnet-20241022-v2:0 (ATUAL)
# Claude 3.5 Sonnet v1: anthropic.claude-3-5-sonnet-20240620-v1:0
# Claude 3 Sonnet: anthropic.claude-3-sonnet-20240229-v1:0
# Claude 3 Haiku: anthropic.claude-3-haiku-20240307-v1:0

# ========================================
# LANGSMITH
# ========================================
def load_langsmith_key() -> str:
    """
    Carrega chave LangSmith do arquivo
    
    Returns:
        str: LangSmith API Key
    """
    key_path = BASE_DIR / "langsmith.key"
    
    if not key_path.exists():
        return os.getenv("LANGSMITH_API_KEY", "")
    
    with open(key_path, 'r') as f:
        return f.read().strip()


LANGSMITH_API_KEY = load_langsmith_key()


# ========================================
# OUTRAS CHAVES (adicione aqui)
# ========================================
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
