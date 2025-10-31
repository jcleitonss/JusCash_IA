from langgraph.graph import StateGraph, END
from typing import TypedDict
from app.models import Processo, DecisionResponse
from app.observability import langsmith_enabled
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.llm_service import llm

print(f"🔍 Workflow - LangSmith habilitado: {langsmith_enabled}")

class WorkflowState(TypedDict):
    processo: Processo
    decision: DecisionResponse | None

prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um analista jurídico especializado em análise de processos para compra de créditos.

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
POL-8: Se faltar documento essencial (ex.: trânsito em julgado não comprovado) → INCOMPLETO

**DECISÕES POSSÍVEIS:**
- "approved": Processo aprovado para compra
- "rejected": Processo rejeitado
- "incomplete": Documentação incompleta

**INSTRUÇÕES:**
1. Analise TODOS os documentos e movimentos
2. Verifique TODAS as políticas POL-1 a POL-8
3. Cite TODAS as políticas relevantes na sua decisão
4. Seja claro e objetivo na justificativa

Retorne APENAS JSON no formato:
{{
  "decision": "approved|rejected|incomplete",
  "rationale": "Justificativa clara citando as políticas",
  "citacoes": ["POL-X", "POL-Y", ...]
}}"""),
    ("user", """Analise o processo abaixo:

{processo}

Retorne a decisão em JSON.""")
])

chain = prompt | llm | JsonOutputParser()

def analyze_node(state: WorkflowState) -> WorkflowState:
    processo_dict = state["processo"].model_dump()
    print(f"📊 Invocando LLM para processo: {processo_dict.get('numeroProcesso')}")
    result = chain.invoke({"processo": processo_dict})
    print(f"✅ LLM respondeu: {result.get('decision')}")
    state["decision"] = DecisionResponse(**result)
    return state

def create_workflow() -> StateGraph:
    workflow = StateGraph(WorkflowState)
    workflow.add_node("analyze", analyze_node)
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", END)
    return workflow.compile()

app_workflow = create_workflow()