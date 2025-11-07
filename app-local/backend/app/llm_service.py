"""
Serviço de integração com AWS Bedrock (Claude 3)
"""
import os
import boto3
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.models import DecisionResponse
from app.observability import langsmith_enabled  # Carrega LangSmith

# Lê credenciais AWS do ambiente
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID', 'us.anthropic.claude-sonnet-4-5-20250929-v1:0')


# Cria cliente Bedrock com credenciais IAM
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Inicializa Bedrock Claude 3.5 Sonnet v2
llm = ChatBedrock(
    client=bedrock_client,
    model_id=BEDROCK_MODEL_ID,
    model_kwargs={
        "temperature": 0,
        "max_tokens": 4096
    }
)

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um analista jurídico especializado em análise de processos judiciais para compra de créditos.

Avalie o processo conforme as POLÍTICAS DE NEGÓCIO:

POL-1: Só compramos crédito de processos transitados em julgado e em fase de execução (OBRIGATÓRIO)
POL-2: Exigir valor de condenação informado (OBRIGATÓRIO)
POL-3: Valor de condenação < R$ 1.000,00 → REJEITAR
POL-4: Condenações na esfera trabalhista → REJEITAR
POL-5: Óbito do autor sem habilitação no inventário → REJEITAR
POL-6: Substabelecimento sem reserva de poderes → REJEITAR
POL-7: Informar honorários contratuais, periciais e sucumbenciais quando existirem (OBRIGATÓRIO)
POL-8: Se faltar documento essencial → INCOMPLETO

DECISÕES POSSÍVEIS:
- "approved": Processo aprovado para compra
- "rejected": Processo rejeitado
- "incomplete": Documentação incompleta

Retorne APENAS JSON no formato:
{
  "decision": "approved|rejected|incomplete",
  "rationale": "Justificativa clara e objetiva",
  "citacoes": ["POL-X", "POL-Y"]
}"""),
    ("user", """PROCESSO:
{processo}

CONTEXTO DE VALIDAÇÃO:
{context}

Analise e retorne a decisão em JSON.""")
])

# Chain com parser JSON
chain = prompt | llm | JsonOutputParser()


def analyze_processo(processo: dict, context: dict) -> DecisionResponse:
    """
    Analisa processo usando Bedrock Claude 3
    
    Args:
        processo: Dados do processo
        context: Contexto de validação prévia
        
    Returns:
        DecisionResponse com decisão estruturada
    """
    # LangSmith rastreia automaticamente
    result = chain.invoke({
        "processo": processo,
        "context": context.get("context", "")
    })
    
    return DecisionResponse(**result)
