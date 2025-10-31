# ⚡ Quick Start - Git Workflow

Guia rápido para usar o sistema de versionamento automatizado.

---

## 🚀 Uso Diário

```bash
cd app-remoto/infrastructure

# Salvar trabalho
make save MSG="feat: nova feature"

# Ver status
make status-git

# Ver versão
make version
```

---

## 📦 Deploy

### **Staging (Testes)**
```bash
make stage
```

### **Produção (Main + AWS)**
```bash
make deploy-prod
# Vai perguntar versão (ou auto-incrementa)
# Faz merge, tag, push e deploy AWS
```

---

## 🔑 Setup Inicial (Uma vez)

### **1. Adicionar token no `keys/.env`:**

```bash
# Já está configurado! Verificar:
cat ../../keys/.env | grep GITHUB_TOKEN
```

### **2. Configurar seu usuário:**

```bash
# Editar keys/.env
GITHUB_USER=seu_usuario_github
GITHUB_REPO=JUSCRASH
```

### **3. Testar:**

```bash
make version
# Deve mostrar versão sem erros
```

---

## 📋 Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `make save MSG="..."` | Salvar em dev |
| `make stage` | Deploy staging |
| `make deploy-prod` | Deploy produção |
| `make status-git` | Ver status |
| `make diff` | Ver mudanças |
| `make changelog` | Gerar changelog |

---

## 🏷️ Versionamento

```bash
# Auto-incrementar
make bump-patch  # 0.1.0 → 0.1.1
make bump-minor  # 0.1.0 → 0.2.0
make bump-major  # 0.1.0 → 1.0.0

# Manual (no deploy-prod)
make deploy-prod
# Digite: 1.0.0
```

---

## ✅ Exemplo Completo

```bash
# 1. Fazer mudanças no código
vim ../agent-core/src/handler.py

# 2. Salvar
cd infrastructure
make save MSG="feat: adiciona endpoint /status"

# 3. Testar em staging
make stage

# 4. Deploy produção
make deploy-prod
# Digite versão: 0.2.0
# Aguarde...
# ✅ Pronto!
```

---

## 🐛 Problemas?

```bash
# Token não funciona?
cat ../../keys/.env | grep GITHUB_TOKEN

# Conflito de merge?
git status
# Resolver manualmente e:
make save MSG="fix: resolve conflicts"

# Ver logs detalhados?
make status-git
```

---

## 📚 Documentação Completa

Ver: [GIT_WORKFLOW.md](./GIT_WORKFLOW.md)

---

**Pronto para usar! 🎉**
