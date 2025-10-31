"""
Pydantic models para validação de dados
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class Documento(BaseModel):
    """Documento do processo"""
    id: str
    dataHoraJuntada: datetime
    nome: str
    texto: str


class Movimento(BaseModel):
    """Movimento processual"""
    dataHora: datetime
    descricao: str


class Processo(BaseModel):
    """Processo judicial completo"""
    numeroProcesso: str = Field(..., description="Número CNJ do processo")
    classe: str
    orgaoJulgador: str
    ultimaDistribuicao: datetime
    assunto: str
    segredoJustica: bool
    justicaGratuita: bool
    siglaTribunal: str
    esfera: str = Field(..., description="Federal, Estadual ou Trabalhista")
    documentos: List[Documento]
    movimentos: List[Movimento]


class DecisionResponse(BaseModel):
    """Resposta da análise do processo"""
    decision: str = Field(..., description="approved, rejected ou incomplete")
    rationale: str = Field(..., description="Justificativa da decisão")
    citacoes: List[str] = Field(..., description="Políticas citadas (POL-X)")
