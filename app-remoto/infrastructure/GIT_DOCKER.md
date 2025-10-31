# 🐳 Git via Docker - Guia Rápido

Sistema Git rodando 100% via Docker (sem precisar instalar Git).

---

## 🚀 Comandos

### **1. Inicializar repositório (primeira vez):**
```bash
git-init.bat
```

### **2. Ver status:**
```bash
git-status.bat
```

### **3. Salvar mudanças:**
```bash
git-save.bat feat: sua mensagem aqui
```

---

## 📋 Exemplos

```bash
# Inicializar
git-init.bat

# Ver o que mudou
git-status.bat

# Salvar
git-save.bat feat: adiciona validação POL-3
git-save.bat fix: corrige bug no Lambda
git-save.bat docs: atualiza README

# Ver status novamente
git-status.bat
```

---

## 🔧 Como funciona

Os scripts `.bat` executam comandos Docker que:
1. Criam container Alpine com Git
2. Montam o projeto como volume
3. Executam comandos Git
4. Fazem push para GitHub usando token de `keys/.env`

---

## ✅ Pronto para usar!

Não precisa instalar Git. Tudo roda via Docker! 🎉
