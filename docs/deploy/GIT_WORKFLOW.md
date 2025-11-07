# 🔄 Git Workflow - JUSCASH

Sistema de versionamento automatizado com Makefile.

---

## 🎯 Workflow

```
dev (desenvolvimento) → staging (testes) → main (produção)
```

---

## 📋 Comandos Principais

### **Desenvolvimento Diário**

```bash
cd app-remoto/infrastructure

# Salvar trabalho em dev
make save MSG="feat: adiciona validação POL-3"
make save MSG="fix: corrige bug no LLM"
make save MSG="docs: atualiza README"
```

---

### **Deploy para Staging**

```bash
# Merge dev → staging
make stage
```

---

### **Deploy para Produção**

```bash
# Merge dev → main + tag + deploy AWS
make prod

# Vai perguntar nova versão (ou auto-incrementa)
# Exemplo: 0.1.0 → 0.1.1
```

---

## 🏷️ Versionamento Semântico

```
v1.2.3
│ │ └─ PATCH: Bugfixes
│ └─── MINOR: Features
└───── MAJOR: Breaking changes
```

### **Incrementar versão:**

```bash
make bump-patch  # 0.1.0 → 0.1.1
make bump-minor  # 0.1.0 → 0.2.0
make bump-major  # 0.1.0 → 1.0.0
```

---

## 📊 Utilitários

```bash
make status-git  # Ver status
make version     # Ver versão atual
make diff        # Ver diferenças dev vs main
make changelog   # Gerar changelog
make branches    # Listar branches
```

---

## 🔐 Credenciais

Configure em `keys/.env`:

```bash
GITHUB_TOKEN=ghp_xxxxx...
GITHUB_USER=seu_usuario
GITHUB_REPO=JUSCRASH
```

⚠️ **NUNCA commitar `keys/.env`!**

---

## 🚀 Exemplo Completo

```bash
# 1. Trabalhar no código
cd app-remoto/infrastructure

# 2. Salvar progresso
make save MSG="feat: implementa POL-3"
make save MSG="test: adiciona testes unitários"

# 3. Testar em staging
make stage

# 4. Deploy produção
make prod
# Digite nova versão: 0.2.0
# Aguarde deploy AWS...
# ✅ Pronto!
```

---

## 📝 Convenção de Commits

```bash
feat:     Nova feature
fix:      Bugfix
docs:     Documentação
test:     Testes
refactor: Refatoração
style:    Formatação
chore:    Manutenção
```

**Exemplos:**
```bash
make save MSG="feat: adiciona validação POL-7"
make save MSG="fix: corrige timeout do Lambda"
make save MSG="docs: atualiza guia de deploy"
```

---

## 🐛 Troubleshooting

### **Erro: GITHUB_TOKEN not found**

```bash
# Verificar
cat ../../keys/.env | grep GITHUB_TOKEN

# Gerar novo: https://github.com/settings/tokens
```

### **Erro: Merge conflict**

```bash
git status
git add .
git commit -m "fix: resolve conflicts"
make save MSG="fix: resolve merge conflicts"
```

---

## 📚 Referências

- **Quickstart:** [QUICKSTART.md](QUICKSTART.md)
- **Terraform:** [TERRAFORM.md](TERRAFORM.md)
- **Backend:** [BACKEND.md](BACKEND.md)
- **Frontend:** [FRONTEND.md](FRONTEND.md)

---

**Autor:** José Cleiton  
**Projeto:** JUSCASH  
**Versão:** 1.0

