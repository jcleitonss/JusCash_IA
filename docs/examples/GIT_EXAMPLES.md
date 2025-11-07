# 💡 Exemplos Práticos - Git Workflow

Cenários reais de uso do sistema de versionamento.

---

## 📝 Cenário 1: Desenvolvimento de Feature

```bash
cd app-remoto/infrastructure

# Dia 1: Começar feature
make save MSG="feat: inicia implementação POL-3"

# Dia 2: Continuar
make save MSG="feat: adiciona validação de valor mínimo"

# Dia 3: Finalizar
make save MSG="feat: completa POL-3 com testes"

# Testar em staging
make stage

# Deploy produção
make deploy-prod
# Versão: 0.2.0
```

---

## 🐛 Cenário 2: Bugfix Urgente

```bash
# 1. Salvar trabalho atual
make save MSG="wip: trabalho em progresso"

# 2. Criar branch de hotfix
git checkout main
git checkout -b hotfix/critical-bug

# 3. Corrigir
vim ../agent-core/src/handler.py

# 4. Commit e push
git add .
git commit -m "fix: corrige timeout do LLM"
git push origin hotfix/critical-bug

# 5. Merge direto na main
git checkout main
git merge hotfix/critical-bug
git push origin main

# 6. Deploy
make deploy-aws

# 7. Voltar para dev
git checkout dev
git merge main
```

---

## 🧪 Cenário 3: Testar Antes de Produção

```bash
# 1. Salvar tudo
make save MSG="feat: múltiplas melhorias"

# 2. Deploy staging
make stage

# 3. Testar manualmente
# https://staging.juscrash.com

# 4. Encontrou problema? Corrigir
make save MSG="fix: ajusta validação"
make stage

# 5. Tudo OK? Produção!
make deploy-prod
```

---

## 🔄 Cenário 4: Rollback

```bash
# Deploy deu problema!

# Ver versões anteriores
git tag

# Fazer rollback
git checkout v0.1.5
make deploy-aws
```

---

## 👥 Cenário 5: Trabalho em Equipe

```bash
# Desenvolvedor A
make save MSG="feat: adiciona endpoint /verify"

# Desenvolvedor B (em outra máquina)
git pull origin dev
make save MSG="feat: adiciona testes"

# Merge automático no próximo deploy
make deploy-prod
```

---

## 📊 Cenário 6: Gerar Release Notes

```bash
# Ver o que mudou desde última versão
make changelog

# Saída:
# - feat: adiciona POL-3
# - fix: corrige timeout
# - docs: atualiza README

# Copiar para release notes
make deploy-prod
# Versão: 1.0.0
```

---

## 🏷️ Cenário 7: Versionamento Semântico

```bash
# Bugfix (patch)
make bump-patch  # 0.1.0 → 0.1.1
make save MSG="fix: pequena correção"
make deploy-prod

# Nova feature (minor)
make bump-minor  # 0.1.1 → 0.2.0
make save MSG="feat: nova funcionalidade"
make deploy-prod

# Breaking change (major)
make bump-major  # 0.2.0 → 1.0.0
make save MSG="feat!: muda API (breaking)"
make deploy-prod
```

---

## 🔍 Cenário 8: Investigar Mudanças

```bash
# Ver o que mudou entre dev e main
make diff

# Ver commits não deployados
make changelog

# Ver status atual
make status-git

# Ver todas as branches
make branches
```

---

## 🚀 Cenário 9: Deploy Completo (Primeira Vez)

```bash
# 1. Configurar credenciais
cat ../../keys/.env

# 2. Inicializar Git
git init
git add .
git commit -m "feat: initial commit"

# 3. Criar repositório no GitHub
# https://github.com/new

# 4. Conectar
git remote add origin https://github.com/SEU_USUARIO/JUSCRASH.git

# 5. Criar branches
git branch -M main
git checkout -b dev
git push -u origin dev
git push -u origin main

# 6. Configurar infraestrutura AWS
cd app-remoto/infrastructure
make init
make apply

# 7. Primeiro deploy
make deploy-prod
# Versão: 0.1.0
```

---

## 🎯 Dicas

### **Mensagens de Commit**

```bash
# Boas práticas
make save MSG="feat: adiciona validação POL-7"
make save MSG="fix: corrige erro no Lambda"
make save MSG="docs: atualiza documentação"
make save MSG="test: adiciona testes unitários"
make save MSG="refactor: melhora performance"
```

### **Quando usar cada comando**

- `make save` → Salvar progresso diário
- `make stage` → Testar antes de produção
- `make deploy-prod` → Deploy final em produção

### **Frequência**

- `save`: Várias vezes por dia
- `stage`: Antes de cada deploy prod
- `deploy-prod`: Quando feature está completa
