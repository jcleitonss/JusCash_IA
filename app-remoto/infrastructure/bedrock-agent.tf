# ========================================
# Amazon Bedrock Agent - JUSCRASH
# ========================================

# IAM Role para Bedrock Agent
resource "aws_iam_role" "bedrock_agent" {
  name = "${var.project_name}-bedrock-agent-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "bedrock.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
  
  tags = {
    Name = "${var.project_name}-bedrock-agent-role"
  }
}

# Policy para invocar modelos Bedrock
resource "aws_iam_role_policy" "bedrock_agent_invoke_model" {
  name = "${var.project_name}-bedrock-agent-invoke-model"
  role = aws_iam_role.bedrock_agent.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "bedrock:InvokeModel"
      Resource = "*"
    }]
  })
}

# Bedrock Agent
resource "aws_bedrockagent_agent" "juscrash_agent" {
  agent_name              = "${var.project_name}-agent"
  agent_resource_role_arn = aws_iam_role.bedrock_agent.arn
  foundation_model        = "anthropic.claude-3-5-sonnet-20240620-v1:0"
  idle_session_ttl_in_seconds = 600
  
  instruction = <<-EOT
Você é um analista jurídico especializado em análise de processos judiciais para compra de créditos.

POLÍTICAS DE NEGÓCIO (POL-1 a POL-8):

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

DECISÕES POSSÍVEIS:
- "approved": Processo aprovado para compra
- "rejected": Processo rejeitado
- "incomplete": Documentação incompleta

INSTRUÇÕES:
1. Analise TODOS os documentos e movimentos do processo
2. Verifique TODAS as políticas POL-1 a POL-8
3. Cite TODAS as políticas relevantes na sua decisão
4. Seja claro e objetivo na justificativa

Retorne APENAS JSON no formato:
{
  "decision": "approved|rejected|incomplete",
  "rationale": "Justificativa clara citando as políticas",
  "citacoes": ["POL-X", "POL-Y", ...]
}
EOT
}

# Agent Alias (Production)
resource "aws_bedrockagent_agent_alias" "production" {
  agent_id         = aws_bedrockagent_agent.juscrash_agent.agent_id
  agent_alias_name = "production"
  description      = "Versão de produção do agente JUSCRASH"
}

# Outputs
output "bedrock_agent_id" {
  description = "ID do Bedrock Agent"
  value       = aws_bedrockagent_agent.juscrash_agent.agent_id
}

output "bedrock_agent_alias_id" {
  description = "ID do Agent Alias (production)"
  value       = aws_bedrockagent_agent_alias.production.agent_alias_id
}

output "bedrock_agent_arn" {
  description = "ARN do Bedrock Agent"
  value       = aws_bedrockagent_agent.juscrash_agent.agent_arn
}
