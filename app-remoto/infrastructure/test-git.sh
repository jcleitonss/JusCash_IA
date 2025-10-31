#!/bin/bash
# Script de teste do sistema Git

echo "🧪 Testando Sistema de Versionamento Git"
echo "=========================================="
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

# Carregar .env
if [ -f "../../keys/.env" ]; then
    source ../../keys/.env
    echo -e "${GREEN}✅ keys/.env carregado${NC}"
else
    echo -e "${RED}❌ keys/.env não encontrado${NC}"
    exit 1
fi

# Testar variáveis
echo ""
echo "📋 Verificando variáveis:"
echo "------------------------"

if [ -n "$GITHUB_TOKEN" ]; then
    echo -e "${GREEN}✅ GITHUB_TOKEN${NC} configurado"
else
    echo -e "${RED}❌ GITHUB_TOKEN${NC} não encontrado"
fi

if [ -n "$GITHUB_USER" ]; then
    echo -e "${GREEN}✅ GITHUB_USER${NC} = $GITHUB_USER"
else
    echo -e "${YELLOW}⚠️  GITHUB_USER${NC} não configurado (atualizar keys/.env)"
fi

if [ -n "$GITHUB_REPO" ]; then
    echo -e "${GREEN}✅ GITHUB_REPO${NC} = $GITHUB_REPO"
else
    echo -e "${RED}❌ GITHUB_REPO${NC} não encontrado"
fi

# Testar Git
echo ""
echo "🔍 Verificando Git:"
echo "-------------------"

if git --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Git instalado${NC}"
else
    echo -e "${RED}❌ Git não instalado${NC}"
    exit 1
fi

# Testar branch
BRANCH=$(git branch --show-current 2>/dev/null)
if [ -n "$BRANCH" ]; then
    echo -e "${GREEN}✅ Branch atual${NC} = $BRANCH"
else
    echo -e "${YELLOW}⚠️  Não está em um repositório Git${NC}"
fi

# Testar versão
echo ""
echo "📦 Verificando versão:"
echo "----------------------"

if [ -f "../.version" ]; then
    VERSION=$(cat ../.version)
    echo -e "${GREEN}✅ Versão${NC} = $VERSION"
else
    echo -e "${YELLOW}⚠️  Arquivo .version não encontrado${NC}"
fi

# Testar Makefile
echo ""
echo "🔧 Verificando Makefile:"
echo "------------------------"

if [ -f "Makefile" ]; then
    echo -e "${GREEN}✅ Makefile encontrado${NC}"
    
    # Testar comando
    if make version > /dev/null 2>&1; then
        echo -e "${GREEN}✅ make version funciona${NC}"
    else
        echo -e "${RED}❌ make version falhou${NC}"
    fi
else
    echo -e "${RED}❌ Makefile não encontrado${NC}"
fi

# Testar GitHub API
echo ""
echo "🌐 Testando GitHub API:"
echo "-----------------------"

if [ -n "$GITHUB_TOKEN" ]; then
    RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user)
    
    if echo "$RESPONSE" | grep -q "login"; then
        LOGIN=$(echo "$RESPONSE" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
        echo -e "${GREEN}✅ Token válido${NC} (usuário: $LOGIN)"
    else
        echo -e "${RED}❌ Token inválido ou expirado${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Token não configurado${NC}"
fi

# Resumo
echo ""
echo "=========================================="
echo "📊 Resumo:"
echo "=========================================="

if [ -n "$GITHUB_TOKEN" ] && [ -n "$GITHUB_USER" ] && [ -f "Makefile" ]; then
    echo -e "${GREEN}✅ Sistema pronto para uso!${NC}"
    echo ""
    echo "Próximos passos:"
    echo "  1. make version"
    echo "  2. make save MSG=\"test: primeiro commit\""
    echo "  3. make help"
else
    echo -e "${YELLOW}⚠️  Configuração incompleta${NC}"
    echo ""
    echo "Ações necessárias:"
    [ -z "$GITHUB_TOKEN" ] && echo "  - Adicionar GITHUB_TOKEN em keys/.env"
    [ -z "$GITHUB_USER" ] && echo "  - Adicionar GITHUB_USER em keys/.env"
    [ ! -f "Makefile" ] && echo "  - Criar Makefile"
fi

echo ""
