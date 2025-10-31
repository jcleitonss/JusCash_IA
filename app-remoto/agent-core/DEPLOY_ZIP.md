# 🚀 Deploy Lambda com ZIP (Sem Docker)

## ✅ Vantagens
- ✅ Sem problemas de Docker manifest no Windows
- ✅ Deploy mais rápido (~30s vs ~5min)
- ✅ Cold start mais rápido (~500ms vs ~2s)
- ✅ Pacote menor (~50MB vs ~500MB)
- ✅ Mais fácil de debugar

---

## 📦 Passo 1: Build do ZIP

### Windows (PowerShell ou CMD):
```bash
cd app-remoto\agent-core
build-zip.bat
```

### Linux/Mac/WSL:
```bash
cd app-remoto/agent-core
bash build-zip.sh
```

**Resultado**: Arquivo `lambda-package.zip` criado (~50MB)

---

## 🏗️ Passo 2: Deploy com Terraform

```bash
cd app-remoto/infrastructure
terraform plan
terraform apply
```

**O que acontece**:
1. Terraform detecta mudança no ZIP (via hash)
2. Faz upload do ZIP para Lambda
3. Atualiza função Lambda
4. Lambda fica pronta em ~30 segundos

---

## 🧪 Passo 3: Testar

### Health Check:
```bash
curl https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/health
```

**Resposta esperada**:
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

### OpenAPI/Swagger:
```
https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/docs
```

### Verificar Processo:
```bash
curl -X POST https://3p6xtd91q4.execute-api.us-east-1.amazonaws.com/prod/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d @test_processo.json
```

---

## 🧹 Passo 4: Limpar ECR (Opcional)

Como não usamos mais Docker, podemos deletar o repositório ECR:

### Via Console AWS:
1. Acesse ECR → Repositories
2. Selecione `juscrash-agent-core`
3. Delete

### Via AWS CLI:
```bash
aws ecr delete-repository \
  --repository-name juscrash-agent-core \
  --force \
  --region us-east-1
```

**Economia**: ~$0.10/GB/mês de armazenamento

---

## 🔄 Workflow de Desenvolvimento

### Fazer mudanças no código:
1. Edite arquivos em `src/`
2. Execute `build-zip.bat` (ou `.sh`)
3. Execute `terraform apply`
4. Teste endpoints

### Rebuild rápido:
```bash
# Windows
cd app-remoto\agent-core && build-zip.bat && cd ..\infrastructure && terraform apply -auto-approve

# Linux/Mac
cd app-remoto/agent-core && bash build-zip.sh && cd ../infrastructure && terraform apply -auto-approve
```

---

## 📊 Comparação: Docker vs ZIP

| Aspecto | Docker (antes) | ZIP (agora) |
|---------|----------------|-------------|
| Build | 5-10 min | 30 seg |
| Deploy | 2-5 min | 30 seg |
| Tamanho | ~500 MB | ~50 MB |
| Cold Start | ~2 seg | ~500 ms |
| Problema Windows | ❌ Manifest error | ✅ Funciona |
| Debug | Difícil | Fácil |

---

## 🐛 Troubleshooting

### Erro: "zip command not found" (Linux/Mac)
```bash
# Ubuntu/Debian
sudo apt-get install zip

# Mac
brew install zip
```

### Erro: "pip: command not found"
```bash
# Instale Python 3.11+
python --version  # Deve ser 3.11+
```

### Erro: "terraform: source_code_hash changed"
**Normal!** Significa que o ZIP mudou. Execute `terraform apply`.

### Lambda retorna erro 500
```bash
# Ver logs
aws logs tail /aws/lambda/juscrash-agent-core --follow
```

---

## 📝 Notas

- O ZIP é criado com dependências para Linux (manylinux2014_x86_64)
- Mangum converte FastAPI para formato Lambda
- Handler correto: `src.handler.handler`
- Tamanho máximo: 250 MB descompactado (estamos em ~150 MB)
