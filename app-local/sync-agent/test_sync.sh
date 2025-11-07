#!/bin/bash
# Script para testar o sync bidirecional corrigido

echo "🧪 Testando Sync Bidirecional Corrigido"
echo "========================================"
echo ""

# 1. Ver estrutura do PostgreSQL
echo "📊 1. Verificando estrutura do PostgreSQL..."
docker exec -it langflow-postgres psql -U langflow -d langflow -f /tmp/debug_postgres.sql

echo ""
echo "✅ 2. Reiniciando sync-agent com código corrigido..."
docker-compose restart sync-agent

echo ""
echo "📋 3. Acompanhando logs (Ctrl+C para sair)..."
docker logs -f juscrash-sync-agent
