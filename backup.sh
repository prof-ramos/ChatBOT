#!/bin/bash

# Script de Backup Automático - ChatBOT Discord
# Faz backup do SQLite database e ChromaDB

set -e

# Configurações
CONTAINER_NAME="discord-chatbot"
BACKUP_DIR="/opt/backups/chatbot"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funções
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar se container está rodando
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    error "Container ${CONTAINER_NAME} não está rodando!"
    exit 1
fi

# Criar diretório de backup
mkdir -p "${BACKUP_DIR}"

log "Iniciando backup do ChatBOT Discord..."

# Backup SQLite Database
log "Fazendo backup do SQLite database..."
if docker exec "${CONTAINER_NAME}" test -f /app/data/sqlite/bot_data.db; then
    docker cp "${CONTAINER_NAME}:/app/data/sqlite/bot_data.db" \
        "${BACKUP_DIR}/bot_data_${DATE}.db"

    # Comprimir
    gzip "${BACKUP_DIR}/bot_data_${DATE}.db"
    log "SQLite backup concluído: bot_data_${DATE}.db.gz"
else
    warning "Arquivo bot_data.db não encontrado no container"
fi

# Backup ChromaDB
log "Fazendo backup do ChromaDB..."
if docker exec "${CONTAINER_NAME}" test -d /app/data/chroma_db; then
    # Criar tar do diretório ChromaDB
    docker exec "${CONTAINER_NAME}" tar czf /tmp/chroma_backup.tar.gz -C /app/data chroma_db

    # Copiar tar para host
    docker cp "${CONTAINER_NAME}:/tmp/chroma_backup.tar.gz" \
        "${BACKUP_DIR}/chroma_db_${DATE}.tar.gz"

    # Limpar arquivo temporário do container
    docker exec "${CONTAINER_NAME}" rm /tmp/chroma_backup.tar.gz

    log "ChromaDB backup concluído: chroma_db_${DATE}.tar.gz"
else
    warning "Diretório chroma_db não encontrado no container"
fi

# Backup da configuração (.env)
if [ -f "$(dirname "$0")/.env" ]; then
    log "Fazendo backup do arquivo .env..."
    cp "$(dirname "$0")/.env" "${BACKUP_DIR}/.env_${DATE}"
    log ".env backup concluído"
fi

# Estatísticas do backup
log "Calculando tamanhos dos backups..."
TOTAL_SIZE=$(du -sh "${BACKUP_DIR}" | cut -f1)
log "Tamanho total dos backups: ${TOTAL_SIZE}"

# Remover backups antigos
log "Removendo backups com mais de ${RETENTION_DAYS} dias..."
find "${BACKUP_DIR}" -name "*.db.gz" -mtime +${RETENTION_DAYS} -delete
find "${BACKUP_DIR}" -name "*.tar.gz" -mtime +${RETENTION_DAYS} -delete
find "${BACKUP_DIR}" -name ".env_*" -mtime +${RETENTION_DAYS} -delete

# Listar backups existentes
BACKUP_COUNT=$(ls -1 "${BACKUP_DIR}"/*.gz 2>/dev/null | wc -l)
log "Total de ${BACKUP_COUNT} arquivos de backup mantidos"

# Upload para cloud (opcional)
if command -v rclone &> /dev/null; then
    if [ -n "${RCLONE_REMOTE}" ]; then
        log "Fazendo upload para ${RCLONE_REMOTE}..."
        rclone copy "${BACKUP_DIR}" "${RCLONE_REMOTE}:/chatbot-backups/" \
            --include "*.gz" \
            --include ".env_*" \
            --max-age 7d
        log "Upload concluído"
    fi
fi

log "Backup finalizado com sucesso!"
log "Backups salvos em: ${BACKUP_DIR}"

# Notificação (opcional)
# Descomentar se quiser enviar notificação via webhook
# if [ -n "${DISCORD_WEBHOOK_URL}" ]; then
#     curl -X POST "${DISCORD_WEBHOOK_URL}" \
#         -H "Content-Type: application/json" \
#         -d "{\"content\": \"✅ Backup do ChatBOT concluído! Total: ${TOTAL_SIZE}\"}"
# fi

exit 0
