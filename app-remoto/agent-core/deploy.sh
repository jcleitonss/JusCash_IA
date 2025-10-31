#!/bin/sh
set -e

echo "🚀 JUSCRASH - Deploy Backend"
echo "=============================="

# Pegar Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="us-east-1"
ECR_URL="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"
REPO_NAME="juscrash-agent-core"

echo ""
echo "📋 Config: $ECR_URL/$REPO_NAME"
echo ""

# Build
echo "🔨 Building..."
cd /workspace
docker build --platform linux/amd64 -t $REPO_NAME .

# Login ECR
echo "🔐 ECR Login..."
aws ecr get-login-password --region $REGION | \
  docker login --username AWS --password-stdin $ECR_URL

# Tag e Push
echo "📦 Pushing..."
docker tag $REPO_NAME:latest $ECR_URL/$REPO_NAME:latest
docker push $ECR_URL/$REPO_NAME:latest

echo ""
echo "✅ Deploy complete!"
echo "Run: terraform apply to update Lambda"
