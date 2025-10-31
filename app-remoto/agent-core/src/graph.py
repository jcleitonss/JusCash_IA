"""
LangGraph workflow para análise de processos
"""
from langgraph.graph import StateGraph, END
from typing import TypedDict
from models import Processo, DecisionResponse
from chains.policy_chain import validate_policies
from chains.llm_chain import analyze


class ProcessoState(TypedDict):
    """Estado do workflow"""
    processo: Processo
    policy_result: dict | None
    decision: DecisionResponse | None


def validate_node(state: ProcessoState) -> ProcessoState:
    """Nó 1: Valida políticas POL-1 a POL-8"""
    state["policy_result"] = validate_policies(state["processo"])
    return state


def should_continue(state: ProcessoState) -> str:
    """Decide se continua para LLM ou rejeita automaticamente"""
    if state["policy_result"]["auto_reject"]:
        return "reject"
    return "analyze"


def analyze_node(state: ProcessoState) -> ProcessoState:
    """Nó 2: Análise via Bedrock Claude"""
    decision = analyze(
        state["processo"].model_dump(),
        state["policy_result"]["context"]
    )
    state["decision"] = decision
    return state


def reject_node(state: ProcessoState) -> ProcessoState:
    """Nó 3: Rejeição automática por política"""
    state["decision"] = DecisionResponse(
        decision="rejected",
        rationale=state["policy_result"]["reason"],
        citacoes=state["policy_result"]["citacoes"]
    )
    return state


def create_workflow() -> StateGraph:
    """Cria e compila o workflow LangGraph"""
    workflow = StateGraph(ProcessoState)
    
    # Adiciona nós
    workflow.add_node("validate", validate_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("reject", reject_node)
    
    # Define fluxo
    workflow.set_entry_point("validate")
    workflow.add_conditional_edges(
        "validate",
        should_continue,
        {
            "analyze": "analyze",
            "reject": "reject"
        }
    )
    workflow.add_edge("analyze", END)
    workflow.add_edge("reject", END)
    
    return workflow.compile()


# Instância global do workflow
app_graph = create_workflow()
