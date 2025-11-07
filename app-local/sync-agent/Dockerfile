FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sync_bidirectional.py .
COPY sync_tradutor.py .
COPY templates/ ./templates/

CMD ["python", "-u", "sync_bidirectional.py"]
