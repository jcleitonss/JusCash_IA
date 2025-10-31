# 🏗️ JUSCRASH Infrastructure (Terraform)

Infraestrutura como código (IaC) para deploy serverless na AWS.

---

## 📦 Recursos Criados

- **S3:** 2 buckets (frontend + flows)
- **CloudFront:** CDN para frontend
- **ECR:** Registry para imagem Docker
- **Lambda:** Function para agent-core
- **API Gateway:** REST API HTTP
- **IAM:** Roles e policies
- **CloudWatch:** Logs

---

## 🚀 Deploy

### **1. Inicializar Terraform**

```bash
terraform init
```

---

### **2. Planejar mudanças**

```bash
terraform plan
```

---

### **3. Aplicar infraestrutura**

```bash
terraform apply
```

Confirme com `yes`.

---

### **4. Ver outputs**

```bash
terraform output
```

Outputs importantes:
- `frontend_url` - URL do CloudFront
- `api_url` - URL da API Gateway
- `ecr_repository_url` - URL do ECR

---

## 📋 Arquivos

```
infrastructure/
├── main.tf           # Provider e backend
├── variables.tf      # Variáveis
├── outputs.tf        # Outputs
├── s3.tf            # Buckets S3
├── cloudfront.tf    # CDN
├── lambda.tf        # Lambda + ECR + IAM
├── apigateway.tf    # API Gateway
└── README.md
```

---

## 🔧 Configuração

### **Backend S3 (State)**

Antes do primeiro `terraform init`, crie o bucket manualmente:

```bash
aws s3 mb s3://juscrash-terraform-state
aws s3api put-bucket-versioning \
  --bucket juscrash-terraform-state \
  --versioning-configuration Status=Enabled
```

---

### **Variáveis**

Edite `variables.tf` ou crie `terraform.tfvars`:

```hcl
aws_region   = "us-east-1"
environment  = "prod"
project_name = "juscrash"
```

---

## 🧪 Validação

### **Verificar recursos criados**

```bash
# Lambda
aws lambda get-function --function-name juscrash-agent-core

# API Gateway
aws apigatewayv2 get-apis

# S3
aws s3 ls | grep juscrash

# CloudFront
aws cloudfront list-distributions
```

---

## 🔄 Atualização

### **Atualizar recurso específico**

```bash
terraform apply -target=aws_lambda_function.agent_core
```

---

### **Ver estado atual**

```bash
terraform show
```

---

### **Ver recursos**

```bash
terraform state list
```

---

## 🗑️ Destruir Infraestrutura

⚠️ **CUIDADO:** Isso deleta TODOS os recursos!

```bash
terraform destroy
```

---

## 💰 Custos Estimados

| Recurso | Custo Mensal |
|---------|--------------|
| S3 (2 GB) | $0.05 |
| CloudFront (100 GB) | $5.00 |
| Lambda (10k requests) | $10.00 |
| API Gateway (10k requests) | $0.35 |
| ECR (500 MB) | $0.05 |
| CloudWatch Logs | $0.50 |
| **TOTAL** | **~$15.95/mês** |

(Não inclui Bedrock - cobrado separadamente)

---

## 🐛 Troubleshooting

### **Erro: Backend not initialized**

```bash
# Criar bucket de state
aws s3 mb s3://juscrash-terraform-state

# Reinicializar
terraform init
```

---

### **Erro: ECR image not found**

O Lambda precisa de uma imagem no ECR antes de ser criado.

**Solução:**

1. Comente o `aws_lambda_function` no `lambda.tf`
2. `terraform apply` (cria ECR)
3. Faça push da imagem (ver `../agent-core/deploy.sh`)
4. Descomente o `aws_lambda_function`
5. `terraform apply` novamente

---

### **Erro: CloudFront takes too long**

CloudFront pode levar 15-20 minutos para provisionar.

```bash
# Ver status
aws cloudfront get-distribution --id E1234567890ABC
```

---

## 📚 Referências

- **Terraform AWS Provider:** https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- **AWS Lambda:** https://docs.aws.amazon.com/lambda/
- **API Gateway:** https://docs.aws.amazon.com/apigateway/
- **CloudFront:** https://docs.aws.amazon.com/cloudfront/

---

## 🔐 Segurança

### **State File**

O `terraform.tfstate` contém informações sensíveis. Nunca commite no Git!

Está configurado para usar S3 backend com versionamento.

---

### **IAM Permissions**

Terraform precisa de permissões para criar:
- S3, CloudFront, Lambda, API Gateway, ECR, IAM, CloudWatch

Use uma role com `AdministratorAccess` ou crie policy customizada.

---

## 📈 Próximos Passos

- [ ] Adicionar WAF (proteção)
- [ ] Custom domain (Route 53)
- [ ] Certificado SSL (ACM)
- [ ] Backup automático
- [ ] Alertas CloudWatch
- [ ] Multi-region
