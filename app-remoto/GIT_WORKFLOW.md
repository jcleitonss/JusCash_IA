# 🔄 Git Workflow - JUSCRASH

Sistema de versionamento automatizado com Makefile.

---

## 🎯 Workflow

```
dev (desenvolvimento) → staging (testes) → main (produção)
```

---

## 📋 Comandos

### **Desenvolvimento Diário**

```bash
cd app-remoto/infrastructure

# Salvar trabalho em dev
make save MSG="feat: adiciona validação POL-3"
make save MSG="fix: corrige bug no LLM"
make save MSG="docs: atualiza README"
```

---

### **Deploy para Staging (Testes)**

```bash
# Merge dev → staging
make stage
```

---

### **Deploy para Produção**

```bash
# Merge dev → main + tag + deploy AWS
make deploy-prod

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

### **Incrementar versão manualmente:**

```bash
make bump-patch  # 0.1.0 → 0.1.1
make bump-minor  # 0.1.0 → 0.2.0
make bump-major  # 0.1.0 → 1.0.0
```

---

## 📊 Utilitários

```bash
# Ver status
make status-git

# Ver versão atual
make version

# Ver diferenças dev vs main
make diff

# Gerar changelog
make changelog

# Listar branches
make branches
```

---

## 🔐 Credenciais

Todas as credenciais estão em `keys/.env`:

```bash
GITHUB_TOKEN=ghp_xxxxx...
GITHUB_USER=seu_usuario
GITHUB_REPO=JUSCRASH
```

⚠️ **NUNCA commitar `keys/.env`!** (já está no .gitignore)

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
make deploy-prod
# Digite nova versão: 0.2.0
# Aguarde deploy AWS...
# ✅ Pronto!
```

---

## 📁 Estrutura

```
JUSCRASH/
├── keys/
│   └── .env                    ← Token GitHub aqui
│
├── app-remoto/
│   ├── .version                ← Versão atual
│   └── infrastructure/
│       └── Makefile            ← Comandos git
│
└── .gitignore                  ← Protege keys/.env
```

---

## 🐛 Troubleshooting

### **Erro: GITHUB_TOKEN not found**

```bash
# Verificar se token está em keys/.env
cat ../../keys/.env | grep GITHUB_TOKEN
```

### **Erro: Permission denied**

```bash
# Token pode estar expirado ou sem permissão
# Gerar novo token: https://github.com/settings/tokens
```

### **Erro: Merge conflict**

```bash
# Resolver conflitos manualmente
git status
git add .
git commit -m "fix: resolve conflicts"
make save MSG="fix: resolve merge conflicts"
```

---

## 📚 Convenção de Commits

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

## ✅ Checklist Deploy Produção

- [ ] Código testado localmente
- [ ] Testes passando
- [ ] Documentação atualizada
- [ ] Changelog gerado
- [ ] Deploy staging OK
- [ ] `make deploy-prod`

---

**Criado por:** José Cleiton  
**Versão:** 1.0.0
