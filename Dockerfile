# Use Python 3.10 slim
FROM python:3.10-slim

# Argumentos de build
ARG DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml ./

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    discord.py==2.3.2 \
    aiohttp==3.9.0 \
    chromadb==0.5.0 \
    openai==2.6.0 \
    pymupdf==1.26.5 \
    python-docx==1.2.0 \
    docx2txt==0.9

# Copiar código da aplicação
COPY main.py database.py vector_db.py import_documents.py ./
COPY documentos_exemplo/ ./documentos_exemplo/

# Criar diretórios para dados persistentes
RUN mkdir -p /app/data/chroma_db /app/data/sqlite

# Variáveis de ambiente (serão sobrescritas no runtime)
ENV PYTHONUNBUFFERED=1
ENV CHROMA_PATH=/app/data/chroma_db

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Comando para iniciar o bot
CMD ["python", "-u", "main.py"]
