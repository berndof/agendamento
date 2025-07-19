# 🧪 Chimera Backend - Ambiente Dockerizado

Este projeto utiliza Docker + Docker Compose para orquestração de ambientes e `make` para automatização de tarefas de desenvolvimento, testes e produção.

---

## ⚙️ Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose (v2+)](https://docs.docker.com/compose/)
- [Make](https://www.gnu.org/software/make/)
- [direnv](https://direnv.net/) (para carregar variáveis automaticamente)
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes Python ultrarrápido)

---

## 📁 Estrutura de Ambientes

- `.env` → Variáveis de infraestrutura usadas pelo Docker (Postgres, Redis etc). Copiado a partir de `.env.dev` pelo `make install`.
- `.env.dev`, `.env.prod` → Templates de ambiente para desenvolvimento e produção.
- `.env.app` → Variáveis usadas diretamente pelo código Python.
- `docker-compose.yml` → Compose base (serviços comuns).
- `docker-compose.dev.yml` → Overrides para ambiente de desenvolvimento.
- `docker-compose.prod.yml` → Overrides para produção.

---

## 🧰 Comandos Disponíveis

Use `make help`



