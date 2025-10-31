#!/bin/bash

# Deploy script para AWS S3

echo "🚀 Deploy Frontend JUSCRASH para AWS S3"
echo ""

# Verificar se .env.production existe
if [ ! -f .env.production ]; then
    echo "❌ Erro: .env.production não encontrado"
    echo "Crie o arquivo com: echo 'VITE_API_URL=https://xxxxx.execute-api.us-east-1.amazonaws.com/prod' > .env.production"
    exit 1
fi

# Build
echo "📦 Building..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build falhou"
    exit 1
fi

# Deploy para S3
echo ""
echo "☁️ Uploading para S3..."
aws s3 sync dist/ s3://juscrash-frontend/ --delete

if [ $? -ne 0 ]; then
    echo "❌ Upload falhou"
    exit 1
fi

# Invalidar CloudFront (opcional)
if [ ! -z "$CLOUDFRONT_DISTRIBUTION_ID" ]; then
    echo ""
    echo "🔄 Invalidando CloudFront cache..."
    aws cloudfront create-invalidation \
        --distribution-id $CLOUDFRONT_DISTRIBUTION_ID \
        --paths "/*"
fi

echo ""
echo "✅ Deploy concluído!"
echo "🌐 URL: http://juscrash-frontend.s3-website-us-east-1.amazonaws.com"
