# 🚀 Deploy Direto para AWS (sem rodar local)

## Pré-requisitos

- Node.js instalado (só para build)
- AWS CLI configurado
- URL da API Gateway (depois do deploy do backend)

---

## 📦 Deploy em 3 comandos

### 1. Instalar dependências (só uma vez)

```bash
cd app-remoto/frontend
npm install
```

### 2. Configurar API URL

```bash
# Criar .env.production com URL da API Gateway
echo VITE_API_URL=https://xxxxx.execute-api.us-east-1.amazonaws.com/prod > .env.production
```

### 3. Build + Deploy

```bash
npm run build
npm run deploy
```

Pronto! ✅

---

## 🌐 Acessar

```
http://juscrash-frontend.s3-website-us-east-1.amazonaws.com
```

---

## ⚡ Ou fazer tudo de uma vez:

```bash
cd app-remoto/frontend
npm install
echo VITE_API_URL=https://xxxxx.execute-api.us-east-1.amazonaws.com/prod > .env.production
npm run build
aws s3 sync dist/ s3://juscrash-frontend/ --delete
```

---

## 📝 Nota

Você **não precisa** rodar `npm run dev` se vai direto para produção.
O `npm install` é só para baixar as dependências necessárias para o build.
