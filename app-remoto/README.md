# ☁️ JUSCRASH - Deploy AWS Serverless

Deploy serverless completo na AWS usando:
- **Frontend:** S3 + CloudFront
- **Backend:** Lambda (Agent Core) + API Gateway + LangGraph
- **Flows:** Git (versionado)
- **LLM:** AWS Bedrock Claude 3
- **Deploy:** Terraform + Makefile

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    AWS Serverless                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CloudFront (CDN)                                       │
│         ↓                                               │
│  S3 (Frontend React)                                    │
│         ↓                                               │
│  API Gateway (REST)                                     │
│         ↓                                               │
│  Lambda (Agent Core + LangGraph)                        │
│    ├─ Carrega flows do Git (JSON)                      │
│    ├─ Valida políticas (POL-1 a POL-8)                 │
│    └─ Análise LLM                                       │
│         ↓                                               │
│  AWS Bedrock (Claude 3.5 Sonnet)                        │
│                                                         │
│  S3 (Terraform State)                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura

```
app-remoto/
│
├── agent-core/                 # Lambda Backend
│   ├── src/
│   │   ├── chains/
│   │   │   ├── policy_chain.py
│   │   │   └── llm_chain.py
│   │   ├── graph.py           # LangGraph workflow
│   │   ├── handler.py         # Lambda entry point
│   │   └── models.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── deploy.sh
│   └── README.md
│
├── frontend/                   # React App
│   ├── src/
│   ├── package.json
│   ├── deploy.sh
│   └── README.md
│
├── infrastructure/             # Terraform IaC
│   ├── Makefile               # Comandos de deploy
│   ├── main.tf
│   ├── s3.tf
│   ├── cloudfront.tf
│   ├── lambda.tf
│   ├── apigateway.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
│
└── README.md                   # Este arquivo
```

---

## 🚀 Deploy Rápido

### **Pré-requisitos**

```bash
# Docker rodando
docker --version

# Credenciais AWS em keys/.env
cat ../../keys/.env
```

---

### **Deploy Completo (Makefile)**

```bash
cd infrastructure

# 1. Simular (dry-run)
make simulate

# 2. Inicializar Terraform
make init

# 3. Criar infraestrutura
make infra

# 4. Deploy aplicação
make deploy
```

---

### **Atualizar Apenas Flows**

```bash
# 1. Sincronizar flows do LangFlow
make sync-flows

# 2. Commit no Git
git add ../../flows/
git commit -m "feat: atualiza workflow"
git push

# 3. Deploy (rebuild Lambda)
make update-flows
```

---

## 💰 Custos Estimados

| Serviço | Uso Mensal | Custo |
|---------|------------|-------|
| **S3** | Frontend + Terraform state | $0.50 |
| **CloudFront** | 100 GB transfer | $5.00 |
| **Lambda** | 10k requests × 1GB × 5s | $5.00 |
| **API Gateway** | 10k requests | $0.35 |
| **Bedrock** | 1M tokens Claude 3 | $15.00 |
| **ECR** | 500 MB | $0.05 |
| **TOTAL** | | **~$25.90/mês** |

---

## 🔧 Configuração

### **Variáveis de Ambiente**

**Backend (Lambda):**
```bash
FLOWS_BUCKET=juscrash-flows
AWS_BEDROCK_REGION=us-east-1
```

**Frontend (React):**
```bash
VITE_API_URL=https://xxxxxx.execute-api.us-east-1.amazonaws.com/prod
```

---

## 📊 Monitoramento

### **CloudWatch Logs**

```bash
# Ver logs do Lambda
aws logs tail /aws/lambda/juscrash-agent-core --follow

# Métricas
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=juscrash-agent-core \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

---

## 🧪 Testes

### **Testar API**

```bash
curl -X POST https://YOUR_API_URL/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d '{
    "numero_processo": "0001234-56.2023.8.26.0100",
    "transitado_julgado": true,
    "fase_execucao": true,
    "valor_condenacao": 50000,
    "esfera": "civel",
    "obito_sem_inventario": false,
    "substabelecimento_sem_reserva": false,
    "honorarios_informados": true
  }'
```

**Resposta esperada:**
```json
{
  "decision": "approved",
  "rationale": "Processo atende todos os critérios...",
  "citacoes": ["POL-1", "POL-2", "POL-7"]
}
```

---

## 🔄 CI/CD

Deploy automático via GitHub Actions quando fizer push na branch `main`.

```bash
git add .
git commit -m "feat: nova feature"
git push origin main
```

GitHub Actions irá:
1. ✅ Build do Docker (backend)
2. ✅ Push para ECR
3. ✅ Update Lambda
4. ✅ Build React (frontend)
5. ✅ Sync S3
6. ✅ Invalidate CloudFront

---

## 🛠️ Comandos Makefile

```bash
cd infrastructure

# Deploy
make simulate       # Simula deploy (dry-run)
make init           # Terraform init
make infra          # Cria infraestrutura
make deploy         # Deploy completo
make deploy-backend # Só backend
make deploy-frontend# Só frontend

# Flows
make sync-flows     # Sincroniza do LangFlow
make update-flows   # Atualiza flows (rebuild)

# Versionamento
make version        # Ver versão atual
make tag V=v1.0.0   # Criar tag
make rollback V=v1.0.0 # Rollback

# Monitoramento
make test           # Testar API
make logs           # Ver logs Lambda
make status         # Status AWS

# Utilitários
make clean          # Limpar temp
make local          # Ambiente local
```

---

## 🐛 Troubleshooting

### **Lambda timeout**

```bash
# Aumentar timeout
aws lambda update-function-configuration \
  --function-name juscrash-agent-core \
  --timeout 120
```

### **Bedrock permission denied**

```bash
# Verificar IAM role
aws iam get-role-policy \
  --role-name juscrash-lambda \
  --policy-name lambda_custom
```

### **CloudFront cache antigo**

```bash
# Invalidar cache
aws cloudfront create-invalidation \
  --distribution-id $(terraform output -raw cloudfront_distribution_id) \
  --paths "/*"
```

---

## 📚 Documentação

- **Agent Core:** [./agent-core/README.md](./agent-core/README.md)
- **Frontend:** [./frontend/README.md](./frontend/README.md)
- **Infrastructure:** [./infrastructure/README.md](./infrastructure/README.md)

---

## 🔐 Segurança

### **Secrets no GitHub**

Configure no repositório:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `ECR_REGISTRY`

### **IAM Permissions**

Lambda precisa de:
- `bedrock:InvokeModel`
- `s3:GetObject` (flows bucket)
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`

---

## 📈 Próximos Passos

- [ ] Adicionar LangSmith (observabilidade)
- [ ] Implementar cache DynamoDB
- [ ] Configurar WAF (proteção)
- [ ] Custom domain (Route 53)
- [ ] Backup automático (S3 versioning)
- [ ] Alertas CloudWatch

---

## 👤 Autor

**José Cleiton**

---

## 📅 Versão

**v1.0.0** - Deploy AWS Serverless
