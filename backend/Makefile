# === Variáveis de ambiente ===
ENV_FILE_DEV := .env.dev
ENV_FILE_PROD := .env.prod

COMPOSE_DEV := docker compose -f docker-compose.yml -f docker-compose.dev.yml --env-file $(ENV_FILE_DEV)
COMPOSE_WATCH := docker compose -f docker-compose.yml -f docker-compose.watch.yml --env-file $(ENV_FILE_DEV)
COMPOSE_PROD := docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file $(ENV_FILE_PROD)

# === Targets padrão ===
.PHONY: help watch up-services run dev down prod-up logs clean nuke

# === Ajuda ===
help:
	@echo "Targets disponíveis:"
	@echo ""
	@echo "  make watch        → Roda o FastAPI em container com watch mode"
	@echo "  make up-services  → Sobe somente serviços (Postgres, Redis)"
	@echo "  make run          → Sobe serviços e roda FastAPI local"
	@echo "  make dev          → Sobe ambiente de desenvolvimento com bind mount do src/ ideal para desenvolver em app/"
	@echo "  make down         → Derruba todos os containers do ambiente"
	@echo "  make prod-up      → Sobe ambiente de produção com build"
	@echo "  make logs         → Mostra logs do container da FastAPI"
	@echo "  make clean        → Limpa containers, redes e volumes"
	@echo "  make nuke         → Apaga tudo: containers, volumes e imagens de build ! USE WITH CAUTION !"

# === Ambiente de Desenvolvimento ===
watch:
	@$(MAKE) down
	@$(COMPOSE_WATCH) build
	@echo "Iniciando Watch Mode ..."
	@bash -c '\
		$(COMPOSE_WATCH) watch & \
		WATCH_PID=$$!; \
		echo "⏳ Aguardando o container iniciar..."; \
		SPIN="|/-\\"; i=0; \
		while ! docker inspect -f "{{.State.Health.Status}}" chimera_backend 2>/dev/null | grep healthy > /dev/null; do \
			i=$$(( (i+1) % 4 )); \
			printf "\r⏳ Aguardando healtchcheck %s" "$${SPIN:$$i:1}"; \
			sleep 0.2; \
		done; \
		printf "\r%*s\r" 90 ""; \
		echo "✅ Container saudável. Exibindo logs..."; \
		docker logs -f chimera_backend & \
		LOGS_PID=$$!; \
		trap "echo 'Encerrando...'; echo ''; kill $$WATCH_PID $$LOGS_PID; exit 0" SIGINT; \
		wait $$LOGS_PID; \
		kill $$WATCH_PID; \
	'



up-services:
	@$(MAKE) down
	@$(COMPOSE_DEV) up -d postgres redis

run:
	@$(MAKE) up-services
	@./src/scripts/run.sh

dev:
	@$(MAKE) down
	@$(COMPOSE_DEV) up -d


down:
	@echo "Derrubando containers (se existirem)..."
	@docker compose down --remove-orphans || echo "⚠️  Nenhum container ativo ou erro ignorado."


clean:
	@echo "🧹 Limpando containers, redes e volumes nomeados..."
	@docker compose down --volumes --remove-orphans || echo "⚠️  Nenhum container ativo."
	@docker volume rm $(docker volume ls -qf dangling=true) 2>/dev/null || true
# === Ambiente de Produção ===

nuke:
	@echo "💣 Apagando tudo: containers, volumes e imagens de build..."
	@docker compose down --volumes --remove-orphans || true
	@docker volume prune -f
	@docker image prune -f

prod-up:
	@$(COMPOSE_PROD) up --build -d

# === Logs ===

logs:
	@docker logs -f chimera_backend
