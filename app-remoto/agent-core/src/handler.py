"""
Lambda Handler - Entry point para AWS Lambda com Bedrock Model
"""
from mangum import Mangum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.models import Processo, DecisionResponse
from src.workflow_bedrock import app_workflow
from src.bedrock_service import get_model_info
from src.observability import langsmith_enabled


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia lifecycle da aplicação"""
    print("🚀 Iniciando JUSCRASH API (Bedrock Model)...")
    if langsmith_enabled:
        print("📊 LangSmith habilitado para observabilidade")
    yield
    print("👋 Encerrando JUSCRASH API...")

app = FastAPI(
    title="JUSCRASH API",
    description="Verificador Inteligente de Processos Judiciais com Bedrock",
    version="2.0.0",
    lifespan=lifespan,
    root_path="/prod"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Health check endpoint"""
    model_info = get_model_info()
    return {
        "status": "ok",
        "service": "juscrash-agent-core",
        "runtime": "aws-lambda",
        "bedrock_model": model_info
    }


@app.post("/api/v1/verificar", response_model=DecisionResponse)
def verificar(processo: Processo):
    """
    Verifica processo judicial conforme políticas POL-1 a POL-8.
    
    Executa workflow LangGraph + Bedrock Model:
    1. LangGraph orquestra o fluxo
    2. Bedrock Model analisa o processo
    3. Retorna decisão estruturada
    
    Returns:
        DecisionResponse com decision, rationale e citacoes
    """
    print("📥 Recebendo processo:", processo.numeroProcesso)
    try:
        result = app_workflow.invoke({
            "processo": processo,
            "decision": None
        })
        
        return result["decision"]
        
    except Exception as e:
        print("❌ Erro:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Erro ao processar processo: " + str(e)
        )


# Mangum adapter para AWS Lambda
import json

def handler(event, context):
    """Lambda handler com logs de debug"""
    print("🔍 EVENT PATH:", event.get('rawPath', event.get('path')))
    print("🔍 METHOD:", event.get('requestContext', {}).get('http', {}).get('method'))
    
    mangum_handler = Mangum(app, lifespan="off")
    response = mangum_handler(event, context)
    
    print("✅ STATUS:", response.get('statusCode'))
    return response
