# === Arquivos de Compose ===
COMPOSE_DEV := docker compose -f docker-compose.yml -f docker-compose.dev.yml
COMPOSE_PROD := docker compose -f docker-compose.yml -f docker-compose.prod.yml

# === Targets ===
.PHONY: help install up-services run dev run-dev down prod-up logs clean nuke

# === Ajuda ===
help:
	@echo ""
	@echo "🚀 Comandos disponíveis:"
	@echo ""
	@echo "  make install      → Prepara o ambiente local (.env.app, dependências, permissões)"
	@echo "  make up-services  → Sobe somente serviços auxiliares (Postgres, Redis) em modo dev"
	@echo "  make run          → Sobe serviços e roda o app FastAPI localmente via script"
	@echo "  make dev          → Sobe ambiente de desenvolvimento (tudo em segundo plano)"
	@echo "  make run-dev      → Sobe ambiente com build + foreground (modo watch ou debug)"
	@echo "  make down         → Derruba todos os containers do ambiente atual"
	@echo "  make prod-up      → Sobe ambiente de produção com build e detach"
	@echo "  make logs         → Mostra logs do container da FastAPI em tempo real"
	@echo "  make clean        → Limpa containers, redes e volumes nomeados"
	@echo "  make nuke         → Apaga tudo: containers, volumes e imagens de build"
	@echo ""

# === Inicialização ===

install:
	@echo "📦 Instalando dependências do projeto..."
	@uv sync
	@chmod +x ./src/scripts/run.sh || true
	@echo "✅ Ambiente preparado."

# === Desenvolvimento ===

up-services:
	@$(MAKE) down
	@$(COMPOSE_DEV) up -d postgres redis

run:
	@$(MAKE) up-services
	@./src/scripts/run.sh

dev:
	@$(COMPOSE_DEV) up -d --build

run-dev:
	@$(COMPOSE_DEV) up --build

down:
	@echo "🛑 Derrubando containers (se existirem)..."
	@docker compose down --remove-orphans || echo "⚠️  Nenhum container ativo ou erro ignorado."

clean:
	@echo "🧹 Limpando containers, redes e volumes nomeados..."
	@docker compose down --volumes --remove-orphans || echo "⚠️  Nenhum container ativo."
	@docker volume rm $$(docker volume ls -qf dangling=true) 2>/dev/null || true

# === Produção ===

prod-up:
	@$(COMPOSE_PROD) up --build -d

# === Logs ===

logs:
	@docker logs -f chimera_backend
