# ⚡ Quick Start - Deploy ZIP

## 🚀 Deploy em 3 Comandos

### Windows (PowerShell/CMD):
```bash
# 1. Build ZIP
cd app-remoto\agent-core
build-zip.bat

# 2. Deploy
cd ..\infrastructure
terraform apply -auto-approve

# 3. Testar
curl https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/health
```

### Linux/Mac/WSL:
```bash
# 1. Build ZIP
cd app-remoto/agent-core
bash build-zip.sh

# 2. Deploy
cd ../infrastructure
terraform apply -auto-approve

# 3. Testar
curl https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/health
```

---

## ✅ Resultado Esperado

```json
{
  "status": "ok",
  "service": "juscrash-agent-core",
  "runtime": "aws-lambda",
  "bedrock_agent": {
    "agent_id": "0NPK3CKUD8",
    "status": "active"
  }
}
```

---

## 📖 Documentação Completa

- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Guia de migração Docker → ZIP
- [agent-core/DEPLOY_ZIP.md](agent-core/DEPLOY_ZIP.md) - Detalhes do deploy ZIP
- [README.md](README.md) - Documentação geral

---

## 🔗 URLs Importantes

| Serviço | URL |
|---------|-----|
| **API Health** | https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/health |
| **OpenAPI/Swagger** | https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/docs |
| **Frontend** | https://d26fvod1jq9hfb.cloudfront.net |
| **CloudWatch Logs** | /aws/lambda/juscrash-agent-core |

---

## 🧪 Testar Verificação de Processo

```bash
curl -X POST https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d '{
    "numeroProcesso": "0001234-56.2023.4.05.8100",
    "classe": "Cumprimento de Sentença",
    "orgaoJulgador": "19ª VARA FEDERAL",
    "ultimaDistribuicao": "2024-11-18T23:15:44.130Z",
    "assunto": "Rural",
    "segredoJustica": false,
    "justicaGratuita": true,
    "siglaTribunal": "TRF5",
    "esfera": "Federal",
    "documentos": [],
    "movimentos": []
  }'
```

---

## 🎯 Tempo Total

- Build ZIP: ~30 segundos
- Terraform apply: ~30 segundos
- **Total: ~1 minuto** 🚀
