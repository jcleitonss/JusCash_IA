@echo off
echo ========================================
echo  JUSCRASH - Deploy Completo
echo  Bedrock Agent + Lambda + Frontend
echo ========================================
echo.

REM Verificar se keys/.env existe
if not exist "..\keys\.env" (
    echo ERRO: Arquivo keys\.env nao encontrado!
    echo Crie o arquivo com as credenciais AWS
    pause
    exit /b 1
)

echo [1/5] Verificando credenciais...
findstr /C:"AWS_ACCESS_KEY_ID" ..\keys\.env >nul
if errorlevel 1 (
    echo ERRO: AWS_ACCESS_KEY_ID nao encontrado em keys\.env
    pause
    exit /b 1
)
echo OK
echo.

echo [2/5] Deploy Infraestrutura (Terraform)...
cd infrastructure
docker compose -f docker-compose.deploy.yml run terraform-init
docker compose -f docker-compose.deploy.yml run terraform-apply
echo.

echo [3/5] Pegando IDs do Bedrock Agent...
docker compose -f docker-compose.deploy.yml run terraform-output > outputs.txt
echo Outputs salvos em infrastructure\outputs.txt
echo.

echo [4/5] Deploy Backend (Lambda)...
docker compose -f docker-compose.deploy.yml run deploy-backend
echo.

echo [5/5] Deploy Frontend (S3 + CloudFront)...
docker compose -f docker-compose.deploy.yml run deploy-frontend
echo.

echo ========================================
echo  DEPLOY CONCLUIDO!
echo ========================================
echo.
echo Proximos passos:
echo 1. Abra infrastructure\outputs.txt
echo 2. Copie bedrock_agent_id e bedrock_agent_alias_id
echo 3. Adicione em keys\.env:
echo    BEDROCK_AGENT_ID=XXXXXXXXXX
echo    BEDROCK_AGENT_ALIAS_ID=XXXXXXXXXX
echo 4. Execute novamente: deploy-all.bat
echo.
pause
