#!/bin/sh
# Script para validar variáveis de ambiente do LangSmith

echo "🔍 Validando configuração LangSmith..."
echo ""

# Carrega .env
if [ -f "../../keys/.env" ]; then
    export $(cat ../../keys/.env | grep -v '^#' | xargs)
    echo "✅ Arquivo .env carregado"
else
    echo "❌ Arquivo ../../keys/.env não encontrado"
    exit 1
fi

echo ""
echo "📊 Variáveis detectadas:"
echo "  LANGSMITH_API_KEY: $([ -n "$LANGSMITH_API_KEY" ] && echo '✅ Presente' || echo '❌ Vazio')"
echo "  LANGSMITH_PROJECT: ${LANGSMITH_PROJECT:-'❌ Não definido'}"
echo "  LANGCHAIN_TRACING_V2: ${LANGCHAIN_TRACING_V2:-'❌ Não definido'}"
echo ""

if [ -z "$LANGSMITH_API_KEY" ]; then
    echo "❌ ERRO: LANGSMITH_API_KEY está vazio!"
    echo "   Edite keys/.env e adicione sua chave"
    exit 1
fi

echo "✅ Configuração válida!"
echo ""
echo "🚀 Pronto para deploy. Execute:"
echo "   docker compose -f docker-compose.deploy.yml run --rm terraform-apply"
