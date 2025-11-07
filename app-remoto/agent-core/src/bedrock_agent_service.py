"""
Serviço de integração com Amazon Bedrock Agent Runtime
"""
import boto3
import json
import os
from typing import Dict, Any

# Configurações do Bedrock Agent
AGENT_ID = os.getenv('BEDROCK_AGENT_ID')
AGENT_ALIAS_ID = os.getenv('BEDROCK_AGENT_ALIAS_ID', 'TSTALIASID')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# Cliente Bedrock Agent Runtime
bedrock_agent_runtime = boto3.client(
    'bedrock-agent-runtime',
    region_name=AWS_REGION
)


def invoke_bedrock_agent(processo_dict: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
    """
    Invoca Bedrock Agent Runtime para análise de processo
    
    Args:
        processo_dict: Dados do processo judicial
        session_id: ID da sessão (opcional, gerado automaticamente)
        
    Returns:
        Resposta do agente com decision, rationale e citacoes
    """
    if not AGENT_ID:
        raise ValueError("BEDROCK_AGENT_ID não configurado")
    
    # Gera session_id se não fornecido
    if not session_id:
        session_id = f"session-{processo_dict.get('numeroProcesso', 'default')}"
    
    # Prepara input para o agente
    input_text = json.dumps(processo_dict, ensure_ascii=False, indent=2)
    
    print("🤖 Invocando Bedrock Agent:", AGENT_ID)
    print("📝 Session ID:", session_id)
    
    # Invoca o agente
    response = bedrock_agent_runtime.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=input_text
    )
    
    # Processa resposta streaming
    result_text = ""
    full_response = []
    
    for event in response['completion']:
        full_response.append(event)
        if 'chunk' in event:
            chunk = event['chunk']
            if 'bytes' in chunk:
                result_text += chunk['bytes'].decode('utf-8')
    
    print("✅ Resposta recebida:", len(result_text), "caracteres")
    print("🔍 Full response:", json.dumps(full_response, default=str)[:500])
    
    # Parse JSON da resposta
    try:
        result_json = json.loads(result_text)
        
        # Se retornou function_calls, extrair do primeiro call
        if 'function_calls' in result_json and len(result_json['function_calls']) > 0:
            first_call = result_json['function_calls'][0]
            if 'arguments' in first_call:
                return first_call['arguments']
        
        return result_json
    except json.JSONDecodeError:
        print("❌ Erro ao parsear JSON:", result_text[:200])
        # Fallback: retorna incomplete
        return {
            "decision": "incomplete",
            "rationale": f"Resposta do agente não está em formato JSON válido. Texto recebido: {result_text[:200]}",
            "citacoes": ["POL-8"]
        }


def get_agent_info() -> Dict[str, Any]:
    """
    Retorna informações sobre o agente configurado
    
    Returns:
        Dicionário com agent_id, alias_id e region
    """
    return {
        "agent_id": AGENT_ID,
        "agent_alias_id": AGENT_ALIAS_ID,
        "region": AWS_REGION,
        "configured": bool(AGENT_ID)
    }
