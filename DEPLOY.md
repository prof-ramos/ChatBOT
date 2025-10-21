# 🚀 Guia de Deploy - Discord Bot RAG v2.0.0

Guia completo para deploy do Discord Bot com RAG em produção usando Docker e Portainer.

## 📋 Pré-requisitos

- ✅ VPS/Servidor com Docker instalado
- ✅ Portainer (opcional, mas recomendado)
- ✅ **Discord Bot Token** - [Criar bot](https://discord.com/developers/applications)
- ✅ **OpenRouter API Key** - [Obter chave](https://openrouter.ai/keys)
- ✅ **OpenAI API Key** - [Obter chave](https://platform.openai.com/api-keys)

## 🏗️ Arquitetura

```
[Discord API] ←──→ [Discord Bot Container]
                        ├── Python App (src/)
                        ├── SQLite DB (volume: chatbot_sqlite)
                        ├── ChromaDB (volume: chatbot_chroma)
                        └── Logs (volume: chatbot_logs)
```

---

## 🚀 Método 1: Deploy com Portainer (Recomendado)

### 1.1 Acessar Portainer

1. Acesse seu Portainer: `https://seu-servidor:9443`
2. Faça login
3. Navegue até **Stacks** → **+ Add stack**

### 1.2 Configurar Stack

**Nome da Stack**: `discord-bot-rag`

**Método**: Selecione uma opção:

#### Opção A: Git Repository (Recomendado)
```
Repository URL: https://github.com/prof-ramos/ChatBOT
Reference: refs/heads/main
Compose path: portainer-stack.yml
```

#### Opção B: Upload
- Faça upload do arquivo `portainer-stack.yml`

#### Opção C: Web Editor
- Cole o conteúdo de `portainer-stack.yml`

### 1.3 Configurar Variáveis de Ambiente

**Variáveis Obrigatórias:**

```env
TOKEN=seu_discord_bot_token_aqui
OPENROUTER_API_KEY=sk-or-v1-xxx
OPENAI_API_KEY=sk-xxx
```

**Variáveis Opcionais:**

```env
# Modelo de IA (padrão: llama-3.1-8b gratuito)
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free

# Modelo de embeddings (padrão: text-embedding-3-small)
EMBEDDING_MODEL=text-embedding-3-small

# Limite de mensagens no histórico (padrão: 10)
CONVERSATION_HISTORY_LIMIT=10

# Documentos RAG retornados (padrão: 2)
RAG_SEARCH_RESULTS=2

# Timezone (padrão: America/Sao_Paulo)
TZ=America/Sao_Paulo
```

### 1.4 Deploy

1. Clique em **Deploy the stack**
2. Aguarde o build da imagem (primeira vez: 3-5 minutos)
3. Verifique os logs em tempo real

### 1.5 Verificar Deploy

**Logs:**
1. **Containers** → `discord-chatbot-rag`
2. Clique em **Logs**
3. Procure por: `Bot conectado como SeuBot`

**Teste no Discord:**
```
@SeuBot !ajuda
@SeuBot Olá, como você está?
```

---

## 🐳 Método 2: Deploy com Docker Compose

### 2.1 Preparar Servidor

```bash
# Conectar via SSH
ssh seu-usuario@seu-servidor.com

# Criar diretório
mkdir -p ~/discord-bot
cd ~/discord-bot

# Clonar repositório
git clone https://github.com/prof-ramos/ChatBOT.git .
```

### 2.2 Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env
nano .env
```

Cole e preencha:

```env
# ===== OBRIGATÓRIAS =====
TOKEN=seu_discord_bot_token
OPENROUTER_API_KEY=sua_chave_openrouter
OPENAI_API_KEY=sua_chave_openai

# ===== OPCIONAIS =====
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
EMBEDDING_MODEL=text-embedding-3-small
CONVERSATION_HISTORY_LIMIT=10
RAG_SEARCH_RESULTS=2
TZ=America/Sao_Paulo
```

Salvar: `Ctrl+O`, `Enter`, `Ctrl+X`

### 2.3 Proteger .env

```bash
chmod 600 .env
```

### 2.4 Build e Deploy

```bash
# Build da imagem
docker-compose build

# Iniciar em background
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f discord-bot
```

### 2.5 Verificar Status

```bash
# Status dos containers
docker-compose ps

# Logs
docker-compose logs --tail 100 discord-bot

# Health check
docker inspect discord-chatbot-rag | grep -A 5 Health
```

---

## 📊 Comandos de Gerenciamento

### Ver Logs

```bash
# Tempo real
docker-compose logs -f

# Últimas 100 linhas
docker-compose logs --tail 100

# Desde 1 hora atrás
docker-compose logs --since 1h

# Apenas erros
docker-compose logs | grep -i error
```

### Restart

```bash
# Via Docker Compose
docker-compose restart

# Via Docker
docker restart discord-chatbot-rag
```

### Atualizar Bot

```bash
cd ~/discord-bot

# Pull latest code
git pull origin main

# Rebuild e restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Acessar Container

```bash
# Shell interativo
docker exec -it discord-chatbot-rag bash

# Executar comando único
docker exec discord-chatbot-rag python --version
```

---

## 💾 Backup e Restore

### Backup Manual

```bash
# Criar diretório de backup
mkdir -p /opt/backups/chatbot

# Backup SQLite
docker run --rm \
  -v chatbot_sqlite:/data \
  -v /opt/backups/chatbot:/backup \
  alpine tar czf /backup/sqlite_$(date +%Y%m%d).tar.gz /data

# Backup ChromaDB
docker run --rm \
  -v chatbot_chroma:/data \
  -v /opt/backups/chatbot:/backup \
  alpine tar czf /backup/chroma_$(date +%Y%m%d).tar.gz /data
```

### Restore

```bash
# Parar bot
docker-compose stop

# Restore SQLite
docker run --rm \
  -v chatbot_sqlite:/data \
  -v /opt/backups/chatbot:/backup \
  alpine sh -c "cd /data && tar xzf /backup/sqlite_YYYYMMDD.tar.gz --strip 1"

# Restore ChromaDB
docker run --rm \
  -v chatbot_chroma:/data \
  -v /opt/backups/chatbot:/backup \
  alpine sh -c "cd /data && tar xzf /backup/chroma_YYYYMMDD.tar.gz --strip 1"

# Reiniciar bot
docker-compose start
```

---

## 🔧 Troubleshooting

### Bot não conecta

```bash
# Verificar token
docker exec discord-chatbot-rag printenv TOKEN

# Ver erros
docker logs discord-chatbot-rag --tail 50 | grep -i error

# Verificar MESSAGE CONTENT INTENT no Discord Developer Portal
# https://discord.com/developers/applications
# Bot → Privileged Gateway Intents → MESSAGE CONTENT INTENT ✅
```

### Container reiniciando

```bash
# Ver estado
docker inspect discord-chatbot-rag | grep -A 10 State

# Logs antes do crash
docker logs discord-chatbot-rag --tail 200

# Rodar em foreground para debug
docker-compose up
```

### Dados não persistem

```bash
# Verificar volumes
docker volume ls | grep chatbot

# Inspecionar volume
docker volume inspect chatbot_sqlite
docker volume inspect chatbot_chroma

# Verificar paths
docker exec discord-chatbot-rag env | grep PATH
```

### Memória insuficiente

```bash
# Ver uso
docker stats discord-chatbot-rag

# Ajustar limite em docker-compose.yml
# deploy.resources.limits.memory: 1G → 2G
```

---

## 🔒 Segurança

### Usuário não-root

O Dockerfile já cria e usa usuário `botuser` (UID 1000)

### Secrets (Produção)

```bash
# Criar secrets
echo "seu_token" | docker secret create discord_token -
echo "sua_key" | docker secret create openrouter_key -
echo "sua_key" | docker secret create openai_key -
```

Modificar `docker-compose.yml`:

```yaml
services:
  discord-bot:
    secrets:
      - discord_token
      - openrouter_key
      - openai_key
    environment:
      - TOKEN_FILE=/run/secrets/discord_token

secrets:
  discord_token:
    external: true
  openrouter_key:
    external: true
  openai_key:
    external: true
```

### Firewall

Bot Discord não precisa de portas expostas (apenas conexões de saída para Discord API)

---

## 📈 Monitoramento (Opcional)

Ver arquivo `docker-compose.monitoring.yml` para Prometheus + Grafana

```bash
# Deploy monitoring
docker-compose -f docker-compose.monitoring.yml up -d

# Acessar Grafana
http://seu-servidor:3000
Login: admin / sua_senha_configurada
```

---

## ✅ Checklist de Deploy

### Pré-Deploy
- [ ] Docker instalado
- [ ] Portainer instalado (opcional)
- [ ] Credenciais obtidas (Discord, OpenRouter, OpenAI)
- [ ] Repositório clonado ou stack configurado

### Deploy
- [ ] `.env` criado e protegido
- [ ] Build bem-sucedido
- [ ] Container rodando
- [ ] Bot conectado (verificar logs)
- [ ] Comandos funcionando (!ajuda, !stats)

### Pós-Deploy
- [ ] Volumes persistindo dados
- [ ] Healthcheck passando
- [ ] Backup configurado
- [ ] Monitoramento configurado (opcional)

---

## 📚 Recursos

- **CLAUDE.md** - Arquitetura técnica detalhada
- **MIGRATION.md** - Guia de migração v1 → v2
- **portainer-stack.yml** - Stack do Portainer
- **docker-compose.yml** - Compose padrão
- **DEPLOY_VPS.md** - Guia avançado de VPS

---

## 🆘 Suporte

### Logs
```bash
docker logs discord-chatbot-rag -f
```

### Comandos de Teste
```
!ajuda
!stats
!rag_stats
```

### Verificar Versão
```bash
docker exec discord-chatbot-rag python -c "from src import __version__; print(__version__)"
```

---

**🎉 Deploy Completo!**

Seu Discord Bot v2.0.0 está rodando em produção com:
- ✅ Estrutura modular e escalável
- ✅ Volumes persistentes
- ✅ Configuração centralizada
- ✅ Health checks
- ✅ Logs estruturados
