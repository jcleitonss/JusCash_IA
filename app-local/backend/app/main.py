"""
FastAPI application - JUSCRASH API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import Processo, DecisionResponse
from app.workflow import app_workflow
from app.observability import langsmith_enabled
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia lifecycle da aplicação"""
    print("🚀 Iniciando JUSCRASH API...")
    if langsmith_enabled:
        print("📊 LangSmith habilitado para observabilidade")
    yield
    print("👋 Encerrando JUSCRASH API...")


# Inicializa FastAPI
app = FastAPI(
    title="JUSCRASH API",
    description="Verificador Inteligente de Processos Judiciais",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
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
    return {
        "status": "ok",
        "service": "juscrash-api",
        "version": "1.0.0"
    }


@app.post("/api/v1/verificar", response_model=DecisionResponse)
def verificar(processo: Processo):
    """
    Verifica processo judicial conforme políticas POL-1 a POL-8.
    
    Executa workflow LangGraph:
    1. Valida políticas de negócio
    2. Análise via LLM (Bedrock Claude 3)
    
    Returns:
        DecisionResponse com decision, rationale e citacoes
    """
    try:
        # Executa workflow LangGraph (LLM analisa todas as políticas)
        result = app_workflow.invoke({
            "processo": processo,
            "decision": None
        })
        
        return result["decision"]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar processo: {str(e)}"
        )
