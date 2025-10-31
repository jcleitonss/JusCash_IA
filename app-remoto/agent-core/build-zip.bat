@echo off
echo 📦 Criando pacote Lambda ZIP...

REM Limpar build anterior
if exist package rmdir /s /q package
if exist lambda-package.zip del lambda-package.zip

REM Criar diretório
mkdir package

REM Instalar dependências
echo 📥 Instalando dependências...
pip install -r requirements.txt -t package\ --platform manylinux2014_x86_64 --only-binary=:all:

REM Copiar código fonte
echo 📋 Copiando código fonte...
xcopy /E /I /Y src package\src

REM Criar ZIP (requer PowerShell)
echo 🗜️ Compactando...
powershell -Command "Compress-Archive -Path package\* -DestinationPath lambda-package.zip -Force"

echo ✅ Pacote criado: lambda-package.zip
echo.
echo 🚀 Próximo passo: cd ..\infrastructure ^&^& terraform apply
