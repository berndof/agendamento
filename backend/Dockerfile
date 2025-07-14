FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Configuração básica
WORKDIR /backend
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/backend
ENV PATH="/backend/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

#instala dependências
COPY pyproject.toml uv.lock ./
COPY src/ /backend/src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

RUN chmod +x scripts/*.sh || true

EXPOSE 9090

#Entrada default (sobreescrita via compose)
CMD ["uv", "run", "main.py"]