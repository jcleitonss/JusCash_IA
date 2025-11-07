@echo off
echo Status do repositorio:
echo.
docker compose -f docker-compose.deploy.yml run --rm git-status
