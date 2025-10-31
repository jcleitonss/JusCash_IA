FROM python:3.11-slim

WORKDIR /app

# Instala dependências
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY backend/app/ ./app/

# Expõe porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
