#!/bin/bash
set -e

echo "📦 Criando pacote Lambda ZIP..."

# Limpar build anterior
rm -rf package lambda-package.zip

# Criar diretório
mkdir package

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt -t package/ --platform manylinux2014_x86_64 --only-binary=:all:

# Copiar código fonte
echo "📋 Copiando código fonte..."
cp -r src package/

# Criar ZIP
echo "🗜️ Compactando..."
cd package
zip -r ../lambda-package.zip . -x "*.pyc" -x "*__pycache__*" -x "*.dist-info/*"
cd ..

# Tamanho
SIZE=$(du -h lambda-package.zip | cut -f1)
echo "✅ Pacote criado: lambda-package.zip ($SIZE)"
echo ""
echo "🚀 Próximo passo: cd ../infrastructure && terraform apply"
