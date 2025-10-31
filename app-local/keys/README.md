# 🔐 Keys - Gerenciamento de Credenciais

Pasta centralizada para armazenar chaves de API e credenciais.

---

## 📁 Arquivos

### `bedrock-long-term-api-key.csv`
Chave de API do AWS Bedrock (formato CSV exportado da AWS)

### `config.py`
Módulo Python que carrega e expõe as credenciais de forma segura

---

## 🔧 Como usar

### No código Python:

```python
# Importar configurações
import sys
sys.path.append('../keys')
from config import BEDROCK_API_KEY, AWS_REGION, BEDROCK_MODEL_ID

# Usar as chaves
print(f"Região: {AWS_REGION}")
print(f"Modelo: {BEDROCK_MODEL_ID}")
```

---

## ➕ Adicionar novas chaves

### 1. Adicionar arquivo de chave:
```
keys/
├── bedrock-long-term-api-key.csv
├── openai-api-key.txt          ← Nova chave
└── config.py
```

### 2. Atualizar `config.py`:
```python
def load_openai_key() -> str:
    """Carrega chave OpenAI"""
    with open(BASE_DIR / "openai-api-key.txt", 'r') as f:
        return f.read().strip()

OPENAI_API_KEY = load_openai_key()
```

---

## ⚠️ Segurança

- ✅ Pasta `keys/` está no `.gitignore`
- ✅ Nunca commitar chaves no Git
- ✅ Usar variáveis de ambiente em produção
- ✅ Rotacionar chaves periodicamente

---

## 🔄 Variáveis de ambiente (alternativa)

Para produção, use `.env`:

```bash
# .env
BEDROCK_API_KEY=ABSKQmVkcm9ja...
AWS_REGION=us-east-1
LANGFUSE_PUBLIC_KEY=pk-...
```

E carregue com:
```python
from dotenv import load_dotenv
load_dotenv()
```
