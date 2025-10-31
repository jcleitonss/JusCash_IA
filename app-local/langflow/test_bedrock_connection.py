"""
Testa conexão com AWS Bedrock usando as mesmas credenciais do docker-compose
"""
import boto3
import json

# Credenciais do docker-compose.yml
AWS_ACCESS_KEY_ID = "AKIAQF53QHFGBNVOHXMC"
AWS_SECRET_ACCESS_KEY = "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"
AWS_REGION = "us-east-1"
MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

print("Testando conexao AWS Bedrock...")
print(f"Regiao: {AWS_REGION}")
print(f"Modelo: {MODEL_ID}")

try:
    # Cria cliente Bedrock
    client = boto3.client(
        service_name='bedrock-runtime',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    
    # Testa chamada
    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 50,
            "messages": [
                {
                    "role": "user",
                    "content": "Diga apenas: Conexão OK"
                }
            ]
        })
    )
    
    result = json.loads(response['body'].read())
    print(f"\nSucesso!")
    print(f"Resposta: {result['content'][0]['text']}")
    print(f"\nLangFlow vai funcionar com essas credenciais!")
    
except Exception as e:
    print(f"\nErro: {e}")
    print(f"\nVerifique as credenciais no docker-compose.yml")
