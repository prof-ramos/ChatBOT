# 🚀 Manual de Deploy em VPS com Portainer e Traefik

Guia completo para deploy do ChatBOT Discord em VPS com Portainer e Traefik já configurados.

## 📋 Pré-requisitos

✅ VPS com Docker e Docker Compose instalados
✅ Portainer instalado e acessível
✅ Traefik instalado e configurado
✅ Domínio (opcional, apenas para Grafana/Prometheus)
✅ Credenciais: Discord Bot Token, OpenRouter API Key, OpenAI API Key

## 🏗️ Arquitetura de Deploy

```
Internet
    ↓
[Traefik] ────────────┐ (Apenas para Grafana/Prometheus)
                      ↓
                 [Grafana:3000]
                 [Prometheus:9090]

[Discord] ←──→ [ChatBOT Container]
                    ├── Python App
                    ├── SQLite DB (volume)
                    ├── ChromaDB (volume)
                    └── Logs (volume)

[Monitoring]
    ├── Prometheus (métricas)
    ├── Grafana (visualização)
    ├── Node Exporter (host metrics)
    └── cAdvisor (container metrics)
```

**Nota**: O bot Discord NÃO precisa de Traefik pois não expõe portas HTTP.

---

## 📦 MÉTODO 1: Deploy via Portainer UI

### 1.1 Preparar Arquivos Localmente

No seu computador, certifique-se que tem todos os arquivos:

```bash
ChatBOT/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.monitoring.yml
├── prometheus.yml
├── .dockerignore
├── backup.sh
├── main.py
├── database.py
├── vector_db.py
└── import_documents.py
```

### 1.2 Upload via Git (Recomendado)

```bash
# Commit todos os arquivos
git add Dockerfile docker-compose.yml docker-compose.monitoring.yml prometheus.yml backup.sh
git commit -m "feat: add Docker and monitoring configuration for VPS deploy"
git push origin main
```

### 1.3 Criar Stack no Portainer

1. **Acesse Portainer**: `https://seu-servidor.com:9443`
2. **Login** com suas credenciais
3. Navegue até **Stacks** (menu lateral esquerdo)
4. Clique em **+ Add stack**

### 1.4 Configurar Stack do ChatBOT

**Nome da Stack**: `chatbot-discord`

**Build method**: Selecione **Repository**

**Configurações**:
- **Repository URL**: `https://github.com/seu-usuario/ChatBOT`
- **Repository reference**: `refs/heads/main`
- **Compose path**: `docker-compose.yml`
- **Auto Update**: ✅ (opcional - atualização automática)

### 1.5 Configurar Environment Variables

Role até **Environment variables** e adicione:

```env
TOKEN=seu_discord_bot_token
OPENROUTER_API_KEY=sua_chave_openrouter
OPENAI_API_KEY=sua_chave_openai
```

OU clique em **Load variables from .env file** e faça upload do seu `.env`

### 1.6 Deploy da Stack

1. Clique em **Deploy the stack**
2. Aguarde o build (primeira vez pode levar 3-5 minutos)
3. Verifique os logs em tempo real

### 1.7 Verificar Deploy

**Ver logs**:
1. Vá em **Containers** no menu lateral
2. Clique em `discord-chatbot`
3. Clique em **Logs**
4. Procure por: `Bot conectado como SeuBot`

**Testar no Discord**:
- Mencione o bot: `@SeuBot !ajuda`
- Ou envie DM: `!stats`

---

## 📦 MÉTODO 2: Deploy via Docker Compose CLI

### 2.1 Conectar na VPS

```bash
ssh seu-usuario@seu-servidor.com
```

### 2.2 Criar Diretório do Projeto

```bash
mkdir -p ~/chatbot-discord
cd ~/chatbot-discord
```

### 2.3 Clonar Repositório

```bash
git clone https://github.com/seu-usuario/ChatBOT.git .
```

### 2.4 Configurar Environment Variables

```bash
nano .env
```

Cole e preencha:

```env
# Discord Bot
TOKEN=seu_discord_bot_token_aqui

# OpenRouter (para chat)
OPENROUTER_API_KEY=sua_chave_openrouter_aqui

# OpenAI (para embeddings)
OPENAI_API_KEY=sua_chave_openai_aqui

# Opcional
EMBEDDING_MODEL=text-embedding-3-small
TZ=America/Sao_Paulo
```

Salve: `Ctrl+O`, `Enter`, `Ctrl+X`

### 2.5 Proteger .env

```bash
chmod 600 .env
```

### 2.6 Build e Deploy

```bash
# Build da imagem Docker
docker-compose build

# Start em background
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f
```

### 2.7 Verificar Status

```bash
# Ver containers rodando
docker-compose ps

# Ver logs dos últimos 100 linhas
docker-compose logs --tail 100

# Ver saúde do container
docker inspect discord-chatbot | grep -A 5 Health
```

---

## 📊 Deploy do Monitoring (Prometheus + Grafana)

### 3.1 Via Portainer UI

1. **Stacks** → **+ Add stack**
2. **Nome**: `chatbot-monitoring`
3. **Build method**: Repository ou Web editor
4. **Compose path**: `docker-compose.monitoring.yml`

**Environment variables**:
```env
DOMAIN=seu-dominio.com
GRAFANA_USER=admin
GRAFANA_PASSWORD=sua_senha_segura
```

5. **Deploy the stack**

### 3.2 Via Docker Compose CLI

```bash
cd ~/chatbot-discord

# Criar .env para monitoring
nano .env.monitoring
```

Cole:
```env
DOMAIN=seu-dominio.com
GRAFANA_USER=admin
GRAFANA_PASSWORD=SuaSenhaSegura123!
```

```bash
# Deploy
docker-compose -f docker-compose.monitoring.yml --env-file .env.monitoring up -d

# Ver logs
docker-compose -f docker-compose.monitoring.yml logs -f
```

### 3.3 Acessar Grafana

**URL**: `https://grafana.seu-dominio.com`

**Login**:
- User: `admin` (ou o que você configurou)
- Password: Sua senha do `.env.monitoring`

### 3.4 Configurar Data Source no Grafana

1. Sidebar → **Configuration** → **Data Sources**
2. **Add data source** → **Prometheus**
3. **URL**: `http://prometheus:9090`
4. **Save & Test**

### 3.5 Importar Dashboards

**Docker Monitoring**:
1. **+** → **Import**
2. Dashboard ID: `193` (Docker monitoring)
3. **Load** → Selecione Prometheus → **Import**

**Node Exporter**:
1. **+** → **Import**
2. Dashboard ID: `1860` (Node Exporter Full)
3. **Load** → **Import**

---

## 🔄 Backup Automático

### 4.1 Tornar Script Executável

```bash
chmod +x backup.sh
```

### 4.2 Testar Backup Manualmente

```bash
./backup.sh
```

Verifique em `/opt/backups/chatbot/`

### 4.3 Configurar Cron Job

```bash
crontab -e
```

Adicione:

```bash
# Backup diário às 3h da manhã
0 3 * * * /root/chatbot-discord/backup.sh >> /var/log/chatbot-backup.log 2>&1

# Backup a cada 6 horas
0 */6 * * * /root/chatbot-discord/backup.sh >> /var/log/chatbot-backup.log 2>&1
```

### 4.4 Backup para Cloud (Opcional)

**Instalar rclone**:

```bash
curl https://rclone.org/install.sh | sudo bash
```

**Configurar Google Drive**:

```bash
rclone config
```

Adicione ao `.env`:

```env
RCLONE_REMOTE=gdrive
```

O script fará upload automático para a cloud!

### 4.5 Restaurar Backup

**Restaurar SQLite**:

```bash
# Parar bot
docker-compose stop

# Restaurar
gunzip -c /opt/backups/chatbot/bot_data_20250121.db.gz | \
    docker cp - discord-chatbot:/app/data/sqlite/bot_data.db

# Reiniciar
docker-compose start
```

**Restaurar ChromaDB**:

```bash
# Parar bot
docker-compose stop

# Limpar ChromaDB existente
docker exec discord-chatbot rm -rf /app/data/chroma_db

# Restaurar
docker cp /opt/backups/chatbot/chroma_db_20250121.tar.gz discord-chatbot:/tmp/
docker exec discord-chatbot tar xzf /tmp/chroma_db_20250121.tar.gz -C /app/data/

# Reiniciar
docker-compose start
```

---

## 🔧 Manutenção e Atualizações

### 5.1 Atualizar Bot (Via Portainer)

1. **Stacks** → `chatbot-discord`
2. Clique em **Pull and redeploy**
3. Aguarde rebuild

### 5.2 Atualizar Bot (Via CLI)

```bash
cd ~/chatbot-discord

# Pull latest code
git pull origin main

# Rebuild e restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 5.3 Ver Logs

**Portainer**:
- Containers → discord-chatbot → Logs

**CLI**:

```bash
# Tempo real
docker-compose logs -f

# Últimas 100 linhas
docker-compose logs --tail 100

# Desde uma hora atrás
docker-compose logs --since 1h

# Apenas erros
docker-compose logs | grep -i error
```

### 5.4 Restart do Bot

**Portainer**:
- Containers → discord-chatbot → Restart

**CLI**:

```bash
docker-compose restart
```

### 5.5 Limpar Recursos

```bash
# Limpar imagens não usadas
docker image prune -a

# Limpar volumes órfãos
docker volume prune

# Limpar tudo (cuidado!)
docker system prune -a --volumes
```

---

## 🔍 Troubleshooting

### ❌ Bot não está conectando

**Sintomas**: Logs mostram erro de autenticação

**Soluções**:

```bash
# 1. Verificar TOKEN
docker exec discord-chatbot printenv TOKEN

# 2. Ver logs de erro
docker logs discord-chatbot --tail 50 | grep -i error

# 3. Verificar intents do Discord
# Vá em: https://discord.com/developers/applications
# Bot → Privileged Gateway Intents → MESSAGE CONTENT INTENT ✅

# 4. Testar conexão manualmente
docker exec -it discord-chatbot python -c "
import os
import discord
token = os.getenv('TOKEN')
print(f'Token configurado: {bool(token)}')
"
```

### ❌ Container reiniciando constantemente

**Sintomas**: Container fica em loop de restart

**Soluções**:

```bash
# 1. Ver motivo do restart
docker inspect discord-chatbot | grep -A 10 State

# 2. Ver últimos logs antes do crash
docker logs discord-chatbot --tail 100

# 3. Desabilitar restart temporariamente
docker update --restart=no discord-chatbot

# 4. Rodar em foreground para debug
docker-compose up

# 5. Acessar container e testar
docker run -it --rm --entrypoint bash discord-chatbot
python main.py
```

### ❌ Dados não estão persistindo

**Sintomas**: Dados somem após restart

**Soluções**:

```bash
# 1. Verificar volumes
docker volume ls | grep chatbot

# 2. Inspecionar volume
docker volume inspect chatbot_sqlite
docker volume inspect chatbot_chroma

# 3. Verificar permissões
docker exec discord-chatbot ls -la /app/data

# 4. Verificar se paths estão corretos
docker exec discord-chatbot env | grep -i path
```

### ❌ Memória insuficiente

**Sintomas**: Container é killed, logs mostram OOMKilled

**Soluções**:

```bash
# 1. Ver uso atual
docker stats discord-chatbot

# 2. Aumentar limite no docker-compose.yml
# Em deploy.resources.limits.memory: mude de 512M para 1G

# 3. Verificar memória do sistema
free -h

# 4. Limitar ChromaDB cache
# Adicione ao .env:
CHROMA_CACHE_SIZE=100
```

### ❌ Grafana não está acessível

**Sintomas**: 404 ou timeout ao acessar grafana.dominio.com

**Soluções**:

```bash
# 1. Verificar se container está rodando
docker ps | grep grafana

# 2. Verificar labels Traefik
docker inspect chatbot-grafana | grep -A 20 Labels

# 3. Ver logs do Traefik
docker logs traefik | grep grafana

# 4. Testar acesso direto
curl -I http://localhost:3000

# 5. Verificar DNS
nslookup grafana.seu-dominio.com
```

### ❌ Prometheus não está coletando métricas

**Sintomas**: Grafana mostra "No Data"

**Soluções**:

```bash
# 1. Acessar Prometheus UI
# http://seu-servidor:9090 (ou via Traefik)

# 2. Verificar targets: Status → Targets
# Todos devem estar "UP"

# 3. Ver logs do Prometheus
docker logs chatbot-prometheus

# 4. Testar scrape manualmente
docker exec chatbot-prometheus wget -O- http://node-exporter:9100/metrics

# 5. Validar prometheus.yml
docker exec chatbot-prometheus promtool check config /etc/prometheus/prometheus.yml
```

---

## 🔒 Segurança

### 6.1 Proteger Grafana com Basic Auth

Edite `docker-compose.monitoring.yml`, adicione:

```yaml
labels:
  - "traefik.http.routers.grafana.middlewares=auth"
  - "traefik.http.middlewares.auth.basicauth.users=admin:$$apr1$$..."
```

Gerar hash:

```bash
htpasswd -nb admin sua_senha
```

### 6.2 Usar Docker Secrets (Mais Seguro)

```bash
# Criar secrets
echo "seu_token" | docker secret create discord_token -
echo "sua_key" | docker secret create openrouter_key -
echo "sua_key" | docker secret create openai_key -
```

Modificar `docker-compose.yml`:

```yaml
services:
  chatbot:
    secrets:
      - discord_token
      - openrouter_key
      - openai_key

secrets:
  discord_token:
    external: true
  openrouter_key:
    external: true
  openai_key:
    external: true
```

### 6.3 Firewall

```bash
# Apenas se necessário expor portas
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 9443/tcp  # Portainer
```

### 6.4 Updates Automáticos

**Watchtower** (atualiza imagens automaticamente):

```bash
docker run -d \
  --name watchtower \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --cleanup \
  --interval 86400  # 24h
```

---

## 📊 Monitoramento Avançado

### 7.1 Alertas no Prometheus

Crie `alerts.yml`:

```yaml
groups:
  - name: chatbot_alerts
    rules:
      - alert: BotDown
        expr: up{job="chatbot"} == 0
        for: 5m
        annotations:
          summary: "ChatBOT Discord está offline"

      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes{name="discord-chatbot"} > 400000000
        for: 10m
        annotations:
          summary: "Bot usando >400MB de memória"
```

### 7.2 Notificações no Grafana

1. **Alerting** → **Notification channels**
2. **Add channel**
3. Tipo: **Discord**, **Slack**, **Email**, etc
4. Configure webhook/SMTP

### 7.3 Métricas Customizadas

Adicione ao `main.py`:

```python
from prometheus_client import Counter, Gauge, start_http_server

# Métricas
messages_total = Counter('discord_messages_total', 'Total de mensagens')
users_active = Gauge('discord_users_active', 'Usuários ativos')

# Start metrics server (porta 8000)
start_http_server(8000)
```

Adicione ao `docker-compose.yml`:

```yaml
ports:
  - "8000:8000"  # Prometheus metrics
```

---

## 📋 Checklist de Deploy

### Pré-Deploy
- [ ] VPS acessível via SSH
- [ ] Docker e Docker Compose instalados
- [ ] Portainer funcionando
- [ ] Traefik configurado (se usar monitoring)
- [ ] Domínio configurado (se usar monitoring)
- [ ] Credenciais Discord/OpenRouter/OpenAI

### Deploy
- [ ] Repositório clonado ou arquivos copiados
- [ ] `.env` criado e protegido (chmod 600)
- [ ] Build da imagem bem-sucedido
- [ ] Container iniciado e rodando
- [ ] Bot conectado ao Discord (ver logs)
- [ ] Teste de comandos: `!ajuda`, `!stats`

### Pós-Deploy
- [ ] Volumes persistindo dados
- [ ] Healthcheck passando
- [ ] Backup configurado (cron job)
- [ ] Monitoring instalado (opcional)
- [ ] Grafana acessível (se configurado)
- [ ] Alertas configurados (opcional)
- [ ] Documentação atualizada

---

## 📚 Comandos Úteis

```bash
# === DOCKER COMPOSE ===

# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Ver logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache

# === DOCKER ===

# Ver containers
docker ps -a

# Ver logs
docker logs discord-chatbot -f

# Acessar shell
docker exec -it discord-chatbot bash

# Ver uso de recursos
docker stats discord-chatbot

# Inspecionar container
docker inspect discord-chatbot

# === VOLUMES ===

# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect chatbot_sqlite

# Backup de volume
docker run --rm -v chatbot_sqlite:/data -v $(pwd):/backup alpine tar czf /backup/sqlite.tar.gz /data

# === NETWORKS ===

# Listar networks
docker network ls

# Inspecionar network
docker network inspect traefik_network

# === SYSTEM ===

# Ver espaço em disco
df -h

# Limpar recursos Docker
docker system prune -a

# Ver uso de disco Docker
docker system df
```

---

## 🆘 Suporte

### Documentação
- [CLAUDE.md](CLAUDE.md) - Arquitetura técnica
- [README.md](README.md) - Docs do usuário
- [CONTRIBUTING.md](CONTRIBUTING.md) - Como contribuir

### Logs
- **Sempre verifique**: `docker logs discord-chatbot`
- **Erros críticos**: `docker logs discord-chatbot | grep -i error`

### Comandos de Teste
- Discord: `!ajuda`, `!stats`, `!rag_stats`
- CLI: `docker exec -it discord-chatbot python -c "import discord; print(discord.__version__)"`

---

**🎉 Deploy Completo!**

Seu ChatBOT Discord está rodando em produção com:
- ✅ Deploy automatizado via Portainer ou CLI
- ✅ Volumes persistentes (SQLite + ChromaDB)
- ✅ Backup automático configurado
- ✅ Monitoring com Prometheus + Grafana
- ✅ Health checks e restart policies
- ✅ Logs centralizados
