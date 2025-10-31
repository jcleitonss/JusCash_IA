# 🎨 JUSCRASH Frontend - AWS Deployment

Frontend React para deploy em S3 + CloudFront.

---

## 🚀 Quick Start

### **Desenvolvimento Local**

```bash
# Instalar dependências
npm install

# Rodar dev server
npm run dev
```

Acesse: http://localhost:5173

---

## ☁️ Deploy AWS

### **Pré-requisitos**

- AWS CLI configurado
- Bucket S3 criado: `juscrash-frontend`
- API Gateway URL (backend)

---

### **1. Configurar API URL**

```bash
# Criar .env.production
echo "VITE_API_URL=https://xxxxx.execute-api.us-east-1.amazonaws.com/prod" > .env.production
```

---

### **2. Build**

```bash
npm run build
```

Gera pasta `dist/` com arquivos estáticos.

---

### **3. Deploy S3**

```bash
# Sync para S3
aws s3 sync dist/ s3://juscrash-frontend/ --delete

# Configurar como site estático
aws s3 website s3://juscrash-frontend \
  --index-document index.html \
  --error-document index.html
```

---

### **4. Tornar Público**

```bash
aws s3api put-bucket-policy \
  --bucket juscrash-frontend \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::juscrash-frontend/*"
    }]
  }'
```

---

### **5. Acessar**

```
http://juscrash-frontend.s3-website-us-east-1.amazonaws.com
```

---

## 🔄 Deploy Automático

```bash
npm run deploy
```

Faz build + sync S3 automaticamente.

---

## 🌐 CloudFront (Opcional)

Para HTTPS e CDN global, configure CloudFront via Terraform:

```bash
cd ../infrastructure
terraform apply
```

Depois invalide o cache:

```bash
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

---

## 📁 Estrutura

```
frontend/
├── src/
│   ├── components/
│   │   ├── ProcessForm.jsx
│   │   ├── ResultCard.jsx
│   │   └── PolicyBadge.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   └── main.jsx
├── public/
├── .env.example
├── .env.development
├── package.json
└── vite.config.js
```

---

## 🔧 Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `VITE_API_URL` | URL da API Gateway | `https://xxxxx.execute-api.us-east-1.amazonaws.com/prod` |

---

## 🐛 Troubleshooting

### **CORS Error**

Configure CORS no API Gateway:
- Allow Origin: `*` ou URL do CloudFront
- Allow Methods: `GET, POST, OPTIONS`
- Allow Headers: `Content-Type`

### **404 em rotas**

Configure error document como `index.html` no S3.

### **Cache antigo**

Invalide CloudFront ou force refresh (Ctrl+Shift+R).

---

## 📚 Tecnologias

- React 18
- Material-UI 5
- Vite 5
- Axios
