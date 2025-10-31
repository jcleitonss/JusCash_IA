# JUSCRASH Frontend

Interface React com Material UI para verificação de processos judiciais.

## 🚀 Rodar Localmente

### Sem Docker

```bash
npm install
npm run dev
```

Acesse: http://localhost:5173

### Com Docker

```bash
# Do diretório app-local (raiz)
cd ..
docker-compose up frontend --build

# Ou apenas frontend isolado
docker-compose up frontend
```

## 🔧 Configuração

Copie `.env.example` para `.env.local`:

```bash
cp .env.example .env.local
```

Edite `VITE_API_URL` para apontar para sua API FastAPI.

## 📦 Build para Produção

```bash
npm run build
```

Os arquivos estarão em `dist/`.

## 🎨 Componentes

- **ProcessForm**: Formulário para entrada de JSON do processo
- **ResultCard**: Exibição do resultado da verificação
- **PolicyBadge**: Badge para políticas citadas

## 🔌 API

Integração com FastAPI em `http://localhost:8000`:

- `POST /api/v1/verificar` - Verificar processo
- `GET /health` - Health check
