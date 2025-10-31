#!/bin/bash
# Script para limpar recursos ECR antigos

REPO_NAME="juscrash-agent-core"
REGION="us-east-1"

echo "🧹 Limpando repositório ECR: $REPO_NAME"
echo ""

# Verificar se repositório existe
if aws ecr describe-repositories --repository-names $REPO_NAME --region $REGION &>/dev/null; then
    echo "📦 Repositório encontrado. Deletando..."
    
    # Deletar repositório (força remoção de imagens)
    aws ecr delete-repository \
        --repository-name $REPO_NAME \
        --force \
        --region $REGION
    
    echo "✅ Repositório ECR deletado com sucesso!"
    echo "💰 Economia estimada: ~$0.10/GB/mês"
else
    echo "ℹ️  Repositório não encontrado (já foi deletado ou nunca existiu)"
fi

echo ""
echo "🎯 Próximos passos:"
echo "   1. Remover referências ao ECR do Terraform (já feito)"
echo "   2. terraform apply (para sincronizar estado)"
