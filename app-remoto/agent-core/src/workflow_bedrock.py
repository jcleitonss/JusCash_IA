"""
Workflow LangGraph com Bedrock Model (invoke_model direto)
"""
from langgraph.graph import StateGraph, END
from typing import TypedDict
from src.models import Processo, DecisionResponse
from src.bedrock_service import invoke_bedrock_model, get_model_info
from src.observability import langsmith_enabled

print("🔍 Workflow - LangSmith habilitado:", langsmith_enabled)


class WorkflowState(TypedDict):
    """Estado do workflow"""
    processo: Processo
    decision: DecisionResponse | None


def analyze_with_bedrock(state: WorkflowState) -> WorkflowState:
    """
    Nó que invoca Bedrock Model para análise
    """
    processo = state["processo"]
    processo_dict = processo.model_dump(mode='json')
    
    print("📊 Analisando processo:", processo_dict.get('numeroProcesso'))
    
    # Invoca Bedrock Model direto
    result = invoke_bedrock_model(processo_dict)
    
    # Converte para DecisionResponse
    state["decision"] = DecisionResponse(**result)
    
    print("✅ Decisão:", state['decision'].decision)
    
    return state


def create_bedrock_workflow() -> StateGraph:
    """
    Cria workflow com Bedrock Model
    """
    model_info = get_model_info()
    print("🤖 Bedrock Model configurado:", model_info['model_id'])
    
    # Cria workflow
    workflow = StateGraph(WorkflowState)
    
    # Adiciona nó único: análise via Bedrock Model
    workflow.add_node("analyze_bedrock", analyze_with_bedrock)
    
    # Define fluxo
    workflow.set_entry_point("analyze_bedrock")
    workflow.add_edge("analyze_bedrock", END)
    
    return workflow.compile()


# Instância global do workflow
app_workflow = create_bedrock_workflow()
