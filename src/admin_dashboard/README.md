# Discord Bot Admin Dashboard

Dashboard administrativo Django para gerenciar o Discord Bot.

## Funcionalidades

### Controle do Bot
- ✅ Ligar/Desligar/Reiniciar bot
- ✅ Status em tempo real (online/offline)
- ✅ Tempo de uptime

### Monitoramento
- ✅ Estatísticas de uso (usuários, mensagens)
- ✅ Métricas de sistema (CPU, memória)
- ✅ Logs em tempo real
- ✅ Export de logs (TXT, JSON)

### Gerenciamento de Embeddings (RAG)
- ✅ Upload de documentos
- ✅ Processamento de embeddings
- ✅ Estatísticas da collection ChromaDB
- ✅ Limpeza de embeddings

### Segurança
- ✅ Autenticação obrigatória
- ✅ Sessões seguras
- ✅ Acesso apenas via localhost

## Acesso

**URL:** http://localhost:8000

**Login padrão:**
- Usuário: `admin`
- Senha: `admin123`

⚠️ **IMPORTANTE:** Altere a senha padrão após o primeiro login!

## Comandos Django

### Criar novo usuário admin
```bash
cd src/admin_dashboard
python manage.py create_admin --username seu_usuario --password sua_senha
```

### Rodar migrações
```bash
python manage.py migrate
```

### Criar superusuário (via prompt)
```bash
python manage.py createsuperuser
```

## Estrutura de Arquivos

```
admin_dashboard/
├── settings.py              # Configurações Django
├── urls.py                  # URLs principais
├── wsgi.py / asgi.py        # Entry points
├── manage.py                # Django CLI
└── admin_panel/             # App principal
    ├── views.py             # Views e APIs
    ├── urls.py              # URLs do app
    ├── bot_manager.py       # Gerenciador do bot
    ├── templates/           # Templates HTML
    │   ├── base.html
    │   ├── dashboard.html
    │   ├── logs.html
    │   ├── embeddings.html
    │   └── login.html
    ├── static/              # Arquivos estáticos
    │   ├── css/style.css
    │   └── js/dashboard.js
    └── management/
        └── commands/
            └── create_admin.py
```

## APIs REST

### Controle do Bot
- `POST /api/bot/start` - Iniciar bot
- `POST /api/bot/stop` - Parar bot
- `POST /api/bot/restart` - Reiniciar bot
- `GET /api/bot/status` - Status atual

### Monitoramento
- `GET /api/stats` - Estatísticas gerais
- `GET /api/uptime` - Tempo online
- `GET /api/logs/stream` - Stream de logs (SSE)
- `GET /api/logs/export?format=txt|json` - Export de logs

### Embeddings
- `GET /api/embeddings/stats` - Estatísticas
- `POST /api/embeddings/process` - Processar documento
- `DELETE /api/embeddings/clear` - Limpar todos

## Desenvolvimento

### Rodar apenas o dashboard (sem bot)
```bash
cd src/admin_dashboard
python manage.py runserver
```

### Coletar arquivos estáticos
```bash
python manage.py collectstatic
```

### Debug mode
Defina a variável de ambiente:
```bash
export DJANGO_DEBUG=True
```
