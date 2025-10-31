# ⚡ Quick Start - 5 Minutos

Deploy JUSCRASH na AWS em 5 comandos.

---

## 1️⃣ Configurar AWS (2 min)

```bash
# Da raiz do projeto
cd JUSCRASH

# Configurar credenciais
docker run --rm -it -v ./keys:/root/.aws amazon/aws-cli configure
```

**Preencher:**
- Access Key ID: `<SUA_KEY>`
- Secret Access Key: `<SUA_SECRET>`
- Region: `us-east-1`
- Output: `json`

---

## 2️⃣ Entrar na pasta (5 seg)

```bash
cd app-remoto/infrastructure
```

---

## 3️⃣ Inicializar (30 seg)

```bash
make init
```

---

## 4️⃣ Criar infraestrutura (15 min)

```bash
make infra
```

Digite `yes` quando pedir confirmação.

---

## 5️⃣ Deploy aplicação (5 min)

```bash
make deploy
```

---

## ✅ Testar

```bash
make test
```

---

## 🎉 Pronto!

Sua aplicação está no ar!

**Ver URLs:**
```bash
make status
```

---

## 📚 Próximos Passos

- Ver logs: `make logs`
- Criar versão: `make tag V=v1.0.0`
- Rollback: `make rollback V=v1.0.0`

**Guia completo:** `DEPLOY.md`
