# JUSCRASH - Makefile para Deploy AWS + Git Versionamento
# Roda da pasta: app-remoto/infrastructure/

# Importar credenciais de keys/.env
include ../../keys/.env
export

VERSION := $(shell cat ../.version 2>/dev/null || echo "0.1.0")
COMMIT := $(shell git rev-parse --short HEAD 2>/dev/null || echo "local")
BRANCH := $(shell git branch --show-current 2>/dev/null || echo "main")
TIMESTAMP := $(shell date +%Y%m%d_%H%M%S)

PROJECT_ROOT := $(shell cd ../.. && pwd)
KEYS_DIR := $(PROJECT_ROOT)/keys

GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
BLUE := \033[0;34m
NC := \033[0m

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$(GREEN)🏛️  JUSCRASH - Deploy AWS + Git$(NC)"
	@echo "Versão: $(VERSION) | Commit: $(COMMIT) | Branch: $(BRANCH)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-18s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Git - Versionamento

.PHONY: save
save: ## Salvar versão em branch dev (uso: make save MSG="feat: nova feature")
	@if [ -z "$(MSG)" ]; then echo "$(RED)❌ Use: make save MSG=\"sua mensagem\"$(NC)"; exit 1; fi
	@echo "$(BLUE)💾 Salvando em branch dev...$(NC)"
	@git checkout dev 2>/dev/null || git checkout -b dev
	@git add .
	@git commit -m "$(MSG) [$(TIMESTAMP)]" || echo "$(YELLOW)Nada para commitar$(NC)"
	@git push https://$(GITHUB_TOKEN)@github.com/$(GITHUB_USER)/$(GITHUB_REPO).git dev
	@echo "$(GREEN)✅ Salvo em dev!$(NC)"

.PHONY: deploy-prod
deploy-prod: ## Deploy para produção (merge dev→main + tag + deploy AWS)
	@echo "$(YELLOW)⚠️  Deploy para PRODUÇÃO?$(NC)"
	@echo "Versão atual: $(VERSION)"
	@read -p "Nova versão (Enter para auto-incrementar patch): " NEW_VERSION; \
	if [ -z "$$NEW_VERSION" ]; then \
		NEW_VERSION=$$(echo $(VERSION) | awk -F. '{$$NF = $$NF + 1;} 1' | sed 's/ /./g'); \
	fi; \
	echo "$$NEW_VERSION" > ../.version; \
	echo "$(BLUE)📦 Versão: $$NEW_VERSION$(NC)"; \
	git checkout main; \
	git merge dev -m "release: v$$NEW_VERSION"; \
	git tag -a "v$$NEW_VERSION" -m "Release v$$NEW_VERSION"; \
	git push https://$(GITHUB_TOKEN)@github.com/$(GITHUB_USER)/$(GITHUB_REPO).git main; \
	git push https://$(GITHUB_TOKEN)@github.com/$(GITHUB_USER)/$(GITHUB_REPO).git "v$$NEW_VERSION"; \
	echo "$(GREEN)✅ Código em produção (main)!$(NC)"; \
	echo "$(BLUE)🚀 Iniciando deploy AWS...$(NC)"; \
	$(MAKE) deploy-aws; \
	git checkout dev

.PHONY: stage
stage: ## Deploy para staging (merge dev→staging)
	@echo "$(BLUE)🧪 Deploy para STAGING...$(NC)"
	@git checkout staging 2>/dev/null || git checkout -b staging
	@git merge dev -m "staging: merge from dev [$(TIMESTAMP)]"
	@git push https://$(GITHUB_TOKEN)@github.com/$(GITHUB_USER)/$(GITHUB_REPO).git staging
	@echo "$(GREEN)✅ Deploy staging completo!$(NC)"
	@git checkout dev

##@ Git - Utilitários

.PHONY: status-git
status-git: ## Ver status do Git
	@echo "$(BLUE)📊 Status Git$(NC)"
	@echo "Branch: $(BRANCH)"
	@echo "Versão: $(VERSION)"
	@echo "Commit: $(COMMIT)"
	@echo ""
	@git status -s

.PHONY: branches
branches: ## Listar branches
	@git branch -a

.PHONY: diff
diff: ## Ver diferenças dev vs main
	@git diff main..dev --stat

.PHONY: changelog
changelog: ## Gerar changelog
	@echo "$(BLUE)📝 Changelog$(NC)"
	@git log main..dev --oneline --pretty=format:"- %s"

##@ AWS - Deploy

.PHONY: deploy-aws
deploy-aws: ## Deploy completo na AWS
	@echo "$(GREEN)🚀 Deploy AWS$(NC)"
	@$(MAKE) deploy-backend
	@$(MAKE) deploy-frontend
	@echo "$(GREEN)✅ Deploy AWS completo!$(NC)"

.PHONY: deploy-backend
deploy-backend: ## Deploy backend Lambda
	@echo "$(GREEN)🤖 Deploy Backend$(NC)"
	@cd ../agent-core && chmod +x deploy.sh && ./deploy.sh

.PHONY: deploy-frontend
deploy-frontend: ## Deploy frontend S3
	@echo "$(GREEN)🎨 Deploy Frontend$(NC)"
	@cd ../../app-local/frontend && npm run build
	@aws s3 sync ../../app-local/frontend/dist/ s3://juscrash-frontend/ --delete

##@ Terraform

.PHONY: init
init: ## Terraform init
	@echo "$(GREEN)🔧 Terraform Init$(NC)"
	@terraform init

.PHONY: plan
plan: ## Terraform plan
	@echo "$(GREEN)📋 Terraform Plan$(NC)"
	@terraform plan

.PHONY: apply
apply: ## Terraform apply
	@echo "$(YELLOW)⚠️  Aplicar mudanças?$(NC)"
	@read -p "Digite 'yes': " confirm; \
	if [ "$$confirm" != "yes" ]; then echo "$(RED)Cancelado$(NC)"; exit 1; fi
	@terraform apply

##@ Monitoramento

.PHONY: logs
logs: ## Ver logs Lambda
	@aws logs tail /aws/lambda/juscrash-agent-core --follow

.PHONY: test-api
test-api: ## Testar API
	@echo "$(GREEN)🧪 Test API$(NC)"
	@curl -s $$(terraform output -raw api_url)/health | jq

##@ Versão

.PHONY: version
version: ## Ver versão atual
	@echo "Versão: $(VERSION)"
	@echo "Commit: $(COMMIT)"
	@echo "Branch: $(BRANCH)"

.PHONY: bump-patch
bump-patch: ## Incrementar patch (0.1.0 → 0.1.1)
	@NEW_VERSION=$$(echo $(VERSION) | awk -F. '{$$NF = $$NF + 1;} 1' | sed 's/ /./g'); \
	echo "$$NEW_VERSION" > ../.version; \
	echo "$(GREEN)Versão: $$NEW_VERSION$(NC)"

.PHONY: bump-minor
bump-minor: ## Incrementar minor (0.1.0 → 0.2.0)
	@NEW_VERSION=$$(echo $(VERSION) | awk -F. '{$$2 = $$2 + 1; $$3 = 0;} 1' | sed 's/ /./g'); \
	echo "$$NEW_VERSION" > ../.version; \
	echo "$(GREEN)Versão: $$NEW_VERSION$(NC)"

.PHONY: bump-major
bump-major: ## Incrementar major (0.1.0 → 1.0.0)
	@NEW_VERSION=$$(echo $(VERSION) | awk -F. '{$$1 = $$1 + 1; $$2 = 0; $$3 = 0;} 1' | sed 's/ /./g'); \
	echo "$$NEW_VERSION" > ../.version; \
	echo "$(GREEN)Versão: $$NEW_VERSION$(NC)"
