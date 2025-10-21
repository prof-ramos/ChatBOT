#!/usr/bin/env bash

# ========================================
# Discord Bot RAG - Stack Deploy Script
# ========================================
#
# Script para deploy automático no Docker Swarm via CLI
# Ideal para CI/CD ou deploy manual rápido
#
# REQUISITOS:
# - Docker Swarm inicializado (docker swarm init)
# - Rede overlay AbduhNet criada (docker network create ...)
# - Arquivo .env configurado
#
# USO:
#   ./stack.deploy.sh              # Deploy com configurações padrão
#   ./stack.deploy.sh --build      # Build da imagem antes do deploy
#   ./stack.deploy.sh --remove     # Remove a stack
#   ./stack.deploy.sh --help       # Mostra esta ajuda
#
# ========================================

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# ========================================
# CONFIGURAÇÕES
# ========================================
STACK_NAME="${COMPOSE_PROJECT_NAME:-discord-bot-rag}"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"
IMAGE_NAME="discord-bot-rag:2.0.0"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ========================================
# FUNÇÕES UTILITÁRIAS
# ========================================

# Print com cores
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Mostra ajuda
show_help() {
    cat << EOF
${GREEN}Discord Bot RAG - Stack Deploy Script${NC}

${BLUE}Uso:${NC}
  $0 [opções]

${BLUE}Opções:${NC}
  --build         Build da imagem antes do deploy
  --remove        Remove a stack do Swarm
  --update        Atualiza serviços existentes (force update)
  --logs          Mostra logs da stack após deploy
  --help          Mostra esta ajuda

${BLUE}Exemplos:${NC}
  $0                    # Deploy simples
  $0 --build            # Build + deploy
  $0 --remove           # Remove stack
  $0 --build --logs     # Build + deploy + logs

${BLUE}Variáveis de ambiente:${NC}
  STACK_NAME          Nome da stack (default: discord-bot-rag)
  COMPOSE_PROJECT_NAME  Sobrescreve STACK_NAME se definido

EOF
    exit 0
}

# Verifica pré-requisitos
check_requirements() {
    info "Verificando pré-requisitos..."

    # Docker instalado?
    if ! command -v docker &> /dev/null; then
        error "Docker não encontrado. Instale: https://docs.docker.com/get-docker/"
    fi

    # Swarm inicializado?
    if ! docker info 2>/dev/null | grep -q "Swarm: active"; then
        error "Docker Swarm não está ativo. Execute: docker swarm init"
    fi

    # Arquivo .env existe?
    if [[ ! -f "$ENV_FILE" ]]; then
        error "Arquivo $ENV_FILE não encontrado. Copie de .env.example e configure."
    fi

    # docker-compose.yml existe?
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        error "Arquivo $COMPOSE_FILE não encontrado."
    fi

    # Rede AbduhNet existe?
    if ! docker network ls | grep -q "AbduhNet"; then
        warn "Rede 'AbduhNet' não encontrada. Criando..."
        docker network create \
            --driver overlay \
            --attachable \
            --label "description=Internal network for Discord bot" \
            AbduhNet
        success "Rede AbduhNet criada."
    fi

    success "Pré-requisitos verificados."
}

# Build da imagem
build_image() {
    info "Building imagem $IMAGE_NAME..."
    docker build \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        -t "$IMAGE_NAME" \
        .
    success "Imagem $IMAGE_NAME construída."
}

# Deploy da stack
deploy_stack() {
    info "Deploying stack '$STACK_NAME'..."

    # Carrega .env e faz deploy
    docker stack deploy \
        --compose-file "$COMPOSE_FILE" \
        --with-registry-auth \
        "$STACK_NAME"

    success "Stack '$STACK_NAME' deployed."

    # Aguarda serviços ficarem prontos
    info "Aguardando serviços ficarem prontos..."
    sleep 5
    docker stack ps "$STACK_NAME" --no-trunc
}

# Remove a stack
remove_stack() {
    info "Removendo stack '$STACK_NAME'..."

    if docker stack ls | grep -q "$STACK_NAME"; then
        docker stack rm "$STACK_NAME"
        success "Stack '$STACK_NAME' removida."

        # Aguarda remoção completa
        info "Aguardando remoção completa..."
        while docker stack ps "$STACK_NAME" 2>/dev/null | grep -q "$STACK_NAME"; do
            sleep 2
            echo -n "."
        done
        echo ""
        success "Stack removida completamente."
    else
        warn "Stack '$STACK_NAME' não existe."
    fi
}

# Força atualização dos serviços
update_services() {
    info "Forçando atualização dos serviços..."

    # Lista serviços da stack
    services=$(docker stack services "$STACK_NAME" --format "{{.Name}}")

    for service in $services; do
        info "Atualizando serviço: $service"
        docker service update --force "$service"
    done

    success "Serviços atualizados."
}

# Mostra logs
show_logs() {
    info "Exibindo logs da stack '$STACK_NAME'..."
    info "Pressione Ctrl+C para sair."
    echo ""

    # Pega o ID do container
    container_id=$(docker ps --filter "label=com.docker.compose.project=$STACK_NAME" --format "{{.ID}}" | head -n1)

    if [[ -n "$container_id" ]]; then
        docker logs -f "$container_id"
    else
        warn "Nenhum container encontrado para a stack '$STACK_NAME'."
    fi
}

# ========================================
# MAIN
# ========================================

main() {
    local do_build=false
    local do_remove=false
    local do_update=false
    local do_logs=false

    # Parse argumentos
    while [[ $# -gt 0 ]]; do
        case $1 in
            --build)
                do_build=true
                shift
                ;;
            --remove)
                do_remove=true
                shift
                ;;
            --update)
                do_update=true
                shift
                ;;
            --logs)
                do_logs=true
                shift
                ;;
            --help|-h)
                show_help
                ;;
            *)
                error "Opção desconhecida: $1. Use --help para ajuda."
                ;;
        esac
    done

    # Banner
    echo -e "${GREEN}"
    cat << "EOF"
╔═══════════════════════════════════════╗
║   Discord Bot RAG - Stack Deploy     ║
║         Docker Swarm Mode            ║
╚═══════════════════════════════════════╝
EOF
    echo -e "${NC}"

    # Executa ações
    check_requirements

    if [[ "$do_remove" == true ]]; then
        remove_stack
        exit 0
    fi

    if [[ "$do_build" == true ]]; then
        build_image
    fi

    deploy_stack

    if [[ "$do_update" == true ]]; then
        update_services
    fi

    if [[ "$do_logs" == true ]]; then
        show_logs
    fi

    echo ""
    success "Deploy concluído com sucesso!"
    echo ""
    info "Comandos úteis:"
    echo "  docker stack ps $STACK_NAME        # Status dos serviços"
    echo "  docker stack services $STACK_NAME  # Lista serviços"
    echo "  docker service logs -f ${STACK_NAME}_discord-bot  # Logs em tempo real"
    echo "  ./stack.deploy.sh --remove         # Remove stack"
    echo ""
}

# Executa main com todos os argumentos
main "$@"
