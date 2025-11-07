FROM public.ecr.aws/lambda/python:3.11

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código mantendo estrutura
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Handler
CMD ["src.handler.handler"]
