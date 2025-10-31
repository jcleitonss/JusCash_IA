# 🚀 Deploy JUSCRASH - Guia Rápido

Deploy via Docker + Makefile da pasta `infrastructure/`.

---

## 📋 Pré-requisitos

1. **Docker Desktop** rodando
2. **Credenciais AWS** em `JUSCRASH/keys/`

---

## 🔐 Configurar Credenciais (Primeira Vez)

```bash
# Da raiz do projeto (JUSCRASH/)
docker run --rm -it -v ./keys:/root/.aws amazon/aws-cli configure

# Preencher:
# AWS Access Key ID: <SUA_KEY>
# AWS Secret Access Key: <SUA_SECRET>
# Default region: us-east-1
# Default output: json
```

**Testar:**
```bash
docker run --rm -v ./keys:/root/.aws:ro amazon/aws-cli sts get-caller-identity
```

---

## 🚀 Deploy em 4 Passos

### **1. Entrar na pasta**
```bash
cd app-remoto/infrastructure
```

---

### **2. Simular (Dry-run)**
```bash
make simulate
```

Mostra o que vai fazer sem executar.

---

### **3. Inicializar Terraform**
```bash
make init
```

Primeira vez apenas.

---

### **4. Criar Infraestrutura**
```bash
make infra
```

Cria: S3, CloudFront, Lambda, API Gateway, ECR.

**Aguarde:** ~15-20 minutos (CloudFront demora).

---

### **5. Deploy Aplicação**
```bash
make deploy
```

Faz:
- Build imagem Lambda
- Push para ECR
- Update Lambda
- Build React
- Sync S3

---

## 📊 Comandos Disponíveis

```bash
make                # Ajuda
make simulate       # Simula deploy
make plan           # Terraform plan
make init           # Terraform init
make infra          # Cria infraestrutura
make deploy         # Deploy completo
make deploy-backend # Só backend
make deploy-frontend# Só frontend
make version        # Mostra versão
make tag V=v1.0.0   # Cria tag Git
make rollback V=v1.0.0 # Rollback
make test           # Testa API
make logs           # Ver logs Lambda
make status         # Status AWS
make clean          # Limpa temp
make local          # Ambiente local
```

---

## 🏷️ Versionamento (Opcional)

### **Criar versão**
```bash
git add .
git commit -m "feat: nova feature"
make tag V=v1.0.0
```

### **Deploy versão**
```bash
make deploy  # Usa tag automaticamente
```

### **Rollback**
```bash
make rollback V=v0.9.0
```

---

## 🧪 Testar

```bash
# Health check
make test

# Logs em tempo real
make logs

# Status
make status
```

---

## 📁 Estrutura de Pastas

```
JUSCRASH/
├── keys/                    # ← Credenciais AWS aqui
│   ├── credentials
│   ├── config
│   └── README.md
│
└── app-remoto/
    └── infrastructure/      # ← Você está aqui
        ├── Makefile         # ← Comandos
        ├── docker-compose.deploy.yml
        ├── *.tf             # Terraform
        └── DEPLOY.md        # Este arquivo
```

---

## 🔄 Fluxo Completo

```bash
# 1. Configurar AWS (primeira vez)
cd JUSCRASH
docker run --rm -it -v ./keys:/root/.aws amazon/aws-cli configure

# 2. Entrar na pasta
cd app-remoto/infrastructure

# 3. Simular
make simulate

# 4. Inicializar
make init

# 5. Criar infraestrutura
make infra

# 6. Deploy
make deploy

# 7. Testar
make test
```

---

## 🐛 Troubleshooting

### **Erro: credentials not found**
```bash
# Verificar
ls -la ../../keys/

# Reconfigurar
docker run --rm -it -v ../../keys:/root/.aws amazon/aws-cli configure
```

### **Erro: Docker daemon not running**
Abra Docker Desktop e aguarde iniciar.

### **Erro: Lambda image not found**
```bash
# Deploy backend primeiro
make deploy-backend
```

---

## 💰 Custos

**Primeiros testes:** ~$0.50

**Uso mensal baixo:** ~$5-10

**Uso mensal médio:** ~$30

---

## 📞 Ajuda

```bash
make help  # Lista todos os comandos
```

**Documentação completa:** `../README.md`
