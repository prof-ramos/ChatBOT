# Multi-stage build for Discord Bot v2.0.0
# Use Python 3.10 slim
FROM python:3.10-slim AS builder

# Argumentos de build
ARG DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema para build
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instalar Poetry e dependências
RUN pip install --no-cache-dir --upgrade pip poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Stage final - imagem de produção
FROM python:3.10-slim

# Metadados
LABEL maintainer="gabriel@example.com"
LABEL version="2.0.0"
LABEL description="Discord Bot with RAG capabilities"

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 botuser && \
    mkdir -p /app/data/chroma_db /app/data/sqlite /app/logs && \
    chown -R botuser:botuser /app

# Definir diretório de trabalho
WORKDIR /app

# Copiar dependências Python do builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código da aplicação (nova estrutura)
COPY --chown=botuser:botuser src/ ./src/
COPY --chown=botuser:botuser scripts/ ./scripts/
COPY --chown=botuser:botuser main.py ./
COPY --chown=botuser:botuser pyproject.toml ./

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CHROMA_DB_PATH=/app/data/chroma_db \
    SQLITE_DB_PATH=/app/data/sqlite/bot_data.db \
    TZ=America/Sao_Paulo

# Mudar para usuário não-root
USER botuser

# Healthcheck - verifica se o processo Python está rodando
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Comando para iniciar o bot
CMD ["python", "-u", "main.py"]
