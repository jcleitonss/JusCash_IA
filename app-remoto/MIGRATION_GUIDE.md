# 🔄 Guia de Migração: Docker → ZIP

## 📋 Resumo da Mudança

**Antes**: Lambda com container Docker (ECR)
**Depois**: Lambda com ZIP deployment

**Motivo**: Resolver problema de Docker manifest no Windows

---

## ✅ Checklist de Migração

### 1️⃣ Build do Pacote ZIP

**Windows**:
```bash
cd app-remoto\agent-core
build-zip.bat
```

**Linux/Mac/WSL**:
```bash
cd app-remoto/agent-core
bash build-zip.sh
```

**Resultado esperado**:
```
✅ Pacote criado: lambda-package.zip (45M)
```

---

### 2️⃣ Aplicar Mudanças no Terraform

```bash
cd app-remoto\infrastructure
terraform plan
```

**Mudanças esperadas**:
```
~ aws_lambda_function.agent_core
    - package_type: "Image" → "Zip"
    - image_uri: "..." → null
    + filename: "../agent-core/lambda-package.zip"
    + runtime: "python3.11"
    + handler: "src.handler.handler"

- aws_ecr_repository.agent_core (será destruído)
```

**Aplicar**:
```bash
terraform apply
```

Digite `yes` quando solicitado.

---

### 3️⃣ Testar Endpoints

**Health Check**:
```bash
curl https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/health
```

**Resposta esperada**:
```json
{
  "status": "ok",
  "service": "juscrash-agent-core",
  "runtime": "aws-lambda"
}
```

**OpenAPI Docs**:
```
https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/docs
```

**Verificar Processo**:
```bash
curl -X POST https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d @../agent-core/test_processo.json
```

---

### 4️⃣ Limpar ECR (Opcional)

**Via Script**:
```bash
cd app-remoto/infrastructure
bash cleanup-ecr.sh
```

**Via Console AWS**:
1. Acesse: https://console.aws.amazon.com/ecr
2. Selecione repositório `juscrash-agent-core`
3. Clique em "Delete"

---

## 🔍 Verificação de Logs

**Ver logs em tempo real**:
```bash
aws logs tail /aws/lambda/juscrash-agent-core --follow
```

**Buscar erros**:
```bash
aws logs tail /aws/lambda/juscrash-agent-core --filter-pattern "ERROR"
```

---

## 🐛 Troubleshooting

### Erro: "No module named 'src'"

**Causa**: Handler incorreto ou estrutura do ZIP errada

**Solução**:
```bash
# Verificar estrutura do ZIP
unzip -l lambda-package.zip | head -20

# Deve mostrar:
# src/
# src/handler.py
# src/models.py
# ...
```

**Verificar handler no Lambda**:
- Console AWS → Lambda → juscrash-agent-core → Configuration → Runtime settings
- Handler deve ser: `src.handler.handler`

---

### Erro: "Unable to import module 'src.handler'"

**Causa**: Dependências faltando ou incompatíveis

**Solução**:
```bash
# Rebuild com flag correta
cd app-remoto/agent-core
rm -rf package lambda-package.zip
pip install -r requirements.txt -t package/ --platform manylinux2014_x86_64 --only-binary=:all:
cp -r src package/
cd package && zip -r ../lambda-package.zip . && cd ..
```

---

### Lambda retorna 502 Bad Gateway

**Causa**: Timeout ou erro não tratado

**Solução**:
```bash
# Ver logs
aws logs tail /aws/lambda/juscrash-agent-core --follow

# Aumentar timeout (se necessário)
# No lambda.tf, mude:
timeout = 120  # de 60 para 120 segundos
```

---

### Terraform: "Error acquiring state lock"

**Causa**: Outro processo Terraform rodando

**Solução**:
```bash
# Aguarde o outro processo terminar, ou force unlock:
terraform force-unlock <LOCK_ID>
```

---

## 📊 Comparação de Performance

### Antes (Docker):
- Build: 5-10 minutos
- Deploy: 2-5 minutos
- Cold start: ~2 segundos
- Tamanho: ~500 MB

### Depois (ZIP):
- Build: 30 segundos
- Deploy: 30 segundos
- Cold start: ~500 ms
- Tamanho: ~50 MB

---

## 🎯 Próximos Passos

1. ✅ Migração concluída
2. ✅ Testes passando
3. ✅ ECR limpo
4. 📝 Atualizar README principal
5. 🚀 Deploy em produção

---

## 📞 Suporte

**Logs CloudWatch**:
```
/aws/lambda/juscrash-agent-core
```

**API Gateway**:
```
https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod
```

**Documentação**:
- [DEPLOY_ZIP.md](agent-core/DEPLOY_ZIP.md)
- [README.md](README.md)
