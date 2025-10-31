@echo off
if "%*"=="" (
    echo Uso: git-save.bat sua mensagem aqui
    echo Exemplo: git-save.bat feat: adiciona nova feature
    exit /b 1
)
echo Salvando mudancas em branch dev...
docker compose -f docker-compose.deploy.yml run --rm -e MSG="%*" git-save
echo.
echo Pronto!
