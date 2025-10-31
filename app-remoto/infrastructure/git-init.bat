@echo off
echo Inicializando repositorio Git...
docker compose -f docker-compose.deploy.yml run --rm git-init
echo.
echo Pronto! Repositorio inicializado.
pause
