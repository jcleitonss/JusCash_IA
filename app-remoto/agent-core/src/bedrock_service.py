"""
Serviço de integração com Amazon Bedrock (invoke_model direto)
"""
import boto3
import json
import os
from typing import Dict, Any

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

# Cliente Bedrock Runtime (não Agent)
bedrock_runtime = boto3.client(
    'bedrock-runtime',
    region_name=AWS_REGION
)

SYSTEM_PROMPT = """Você é um analista jurídico especializado em análise de processos para compra de créditos.

Avalie o processo conforme as POLÍTICAS DE NEGÓCIO:

**Regra-base (elegibilidade)**
POL-1: Só compramos crédito de processos transitados em julgado e em fase de execução (OBRIGATÓRIO)
POL-2: Exigir valor de condenação informado (OBRIGATÓRIO)

**Quando NÃO compramos o crédito**
POL-3: Valor de condenação < R$ 1.000,00 → REJEITAR
POL-4: Condenações na esfera trabalhista → REJEITAR
POL-5: Óbito do autor sem habilitação no inventário → REJEITAR
POL-6: Substabelecimento sem reserva de poderes → REJEITAR

**Honorários**
POL-7: Informar honorários contratuais, periciais e sucumbenciais quando existirem (OBRIGATÓRIO)

**Qualidade**
POL-8: Se faltar documento essencial → INCOMPLETO

Retorne APENAS um objeto JSON válido, sem texto adicional:
{
  "decision": "approved|rejected|incomplete",
  "rationale": "Justificativa clara citando as políticas",
  "citacoes": ["POL-X", "POL-Y"]
}"""


def invoke_bedrock_model(processo_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invoca Bedrock Model diretamente (sem Agent)
    
    Args:
        processo_dict: Dados do processo judicial
        
    Returns:
        Resposta com decision, rationale e citacoes
    """
    print("🤖 Invocando Bedrock Model:", MODEL_ID)
    
    # Monta prompt
    user_message = f"Analise o processo abaixo:\n\n{json.dumps(processo_dict, ensure_ascii=False, indent=2)}"
    
    # Payload para Claude
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "temperature": 0.1,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ]
    }
    
    # Invoca modelo
    response = bedrock_runtime.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(payload)
    )
    
    # Parse resposta
    response_body = json.loads(response['body'].read())
    
    # Extrai texto da resposta
    content = response_body.get('content', [])
    if content and len(content) > 0:
        result_text = content[0].get('text', '')
    else:
        result_text = ""
    
    print("✅ Resposta recebida:", len(result_text), "caracteres")
    
    # Parse JSON
    try:
        # Remove markdown se houver
        if result_text.startswith('```json'):
            result_text = result_text.split('```json')[1].split('```')[0].strip()
        elif result_text.startswith('```'):
            result_text = result_text.split('```')[1].split('```')[0].strip()
        
        result_json = json.loads(result_text)
        return result_json
    except json.JSONDecodeError as e:
        print("❌ Erro ao parsear JSON:", str(e))
        print("Texto recebido:", result_text[:500])
        return {
            "decision": "incomplete",
            "rationale": f"Erro ao processar resposta do modelo: {str(e)}",
            "citacoes": ["POL-8"]
        }


def get_model_info() -> Dict[str, Any]:
    """
    Retorna informações sobre o modelo configurado
    """
    return {
        "model_id": MODEL_ID,
        "region": AWS_REGION,
        "configured": True
    }
