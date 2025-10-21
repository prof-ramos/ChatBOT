# Discord Bot Admin Dashboard - Quick Start

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
# Com Poetry (recomendado)
poetry install

# Ou com pip
pip install -r requirements.txt  # Se você tiver um requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Discord
TOKEN=seu_token_discord_aqui

# OpenRouter (AI)
OPENROUTER_API_KEY=sua_chave_openrouter
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free

# OpenAI (Embeddings)
OPENAI_API_KEY=sua_chave_openai

# Django (opcional)
DJANGO_SECRET_KEY=chave_secreta_aleatoria
DJANGO_DEBUG=True
```

### 3. Iniciar Bot + Dashboard

```bash
# Opção 1: Script conveniente
./start_dashboard.sh

# Opção 2: Diretamente
python main.py

# Opção 3: Com Poetry
poetry run python main.py
```

### 4. Acessar Dashboard

1. Abra seu navegador em: **http://localhost:8000**
2. Faça login com credenciais padrão:
   - **Usuário:** `admin`
   - **Senha:** `admin123`
3. ⚠️ **IMPORTANTE:** Altere a senha após o primeiro login!

## 📊 Funcionalidades do Dashboard

### Controle do Bot
- **Ligar/Desligar/Reiniciar** o bot com um clique
- **Status em tempo real** (online/offline)
- **Tempo de uptime** (quanto tempo o bot está rodando)

### Monitoramento
- **Estatísticas de uso:**
  - Total de usuários
  - Total de mensagens
  - Mensagens de usuários vs respostas do bot
- **Métricas do sistema:**
  - Uso de CPU
  - Uso de memória
- **Auto-refresh** a cada 5 segundos

### Logs
- **Visualização em tempo real** dos logs do bot
- **Export de logs** em formato TXT ou JSON
- **Auto-refresh** opcional
- **Últimas 50 linhas** sempre visíveis

### Gerenciamento de Embeddings (RAG)
- **Upload de documentos** (TXT, PDF, DOCX)
- **Processar embeddings** para RAG
- **Estatísticas:**
  - Número de documentos processados
  - Status da collection ChromaDB
- **Limpar embeddings** (ação destrutiva!)

## 🎯 Workflow Típico

### Primeira Vez
1. Instalar dependências
2. Configurar `.env`
3. Executar `python main.py`
4. Acessar dashboard e fazer login
5. Clicar em "Ligar Bot"
6. Bot estará online no Discord

### Uso Diário
1. Executar `python main.py`
2. Acessar dashboard
3. Verificar status do bot
4. Ligar bot se necessário
5. Monitorar logs e estatísticas

### Adicionar Documentos ao RAG
1. Ir para página "Embeddings"
2. Fazer upload de documento
3. Clicar em "Processar Documento"
4. Aguardar confirmação
5. Bot agora pode responder perguntas sobre o documento

## 🛠️ Comandos Úteis

### Criar Novo Usuário Admin
```bash
cd src/admin_dashboard
python manage.py create_admin --username seu_usuario --password sua_senha
```

### Alterar Senha de Usuário Existente
```bash
cd src/admin_dashboard
python manage.py changepassword admin
```

### Ver Logs do Django
Os logs estão em: `logs/discord_bot.log`

```bash
# Ver últimas linhas
tail -f logs/discord_bot.log

# Ver erros
tail -f logs/discord_bot_error.log
```

### Resetar Dashboard (Limpar Dados)
```bash
# Remove banco de dados do dashboard (NÃO afeta dados do bot)
rm admin_dashboard.db

# Re-executar migrações
cd src/admin_dashboard
python manage.py migrate
python manage.py create_admin
```

## 🔒 Segurança

### Trocar Senha Padrão
**MUITO IMPORTANTE:** Sempre altere a senha padrão!

```bash
cd src/admin_dashboard
python manage.py changepassword admin
```

### Acesso Remoto (Não Recomendado)
Por padrão, o dashboard só aceita conexões de `localhost` (127.0.0.1).

Se você REALMENTE precisa de acesso remoto:

1. Edite `src/admin_dashboard/settings.py`:
   ```python
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'seu.dominio.com']
   ```

2. Configure variáveis de segurança:
   ```env
   DJANGO_SECRET_KEY=chave_super_secreta_aleatoria_aqui
   DJANGO_DEBUG=False
   ```

3. Use HTTPS/reverse proxy (Nginx, Caddy, etc.)

## 📝 Estrutura de Arquivos

```
ChatBOT/
├── src/
│   ├── discord_bot/          # Bot Discord
│   └── admin_dashboard/      # Dashboard Django
│       ├── admin_panel/
│       │   ├── templates/    # HTML
│       │   └── static/       # CSS/JS
│       └── settings.py       # Configuração Django
├── logs/                     # Logs do bot
│   ├── discord_bot.log       # Todos os logs
│   └── discord_bot_error.log # Apenas erros
├── bot_data.db              # Dados do bot (conversas, usuários)
├── admin_dashboard.db       # Dados do dashboard (auth)
├── main.py                  # Entry point
└── start_dashboard.sh       # Script de inicialização
```

## 🐛 Problemas Comuns

### "No module named 'django'"
```bash
poetry install
# ou
pip install django django-cors-headers whitenoise psutil
```

### "CSRF verification failed"
- Certifique-se de fazer login novamente
- Limpe cookies do navegador
- Verifique se está acessando via http://localhost:8000

### Bot não liga pelo dashboard
- Verifique se `TOKEN` está configurado no `.env`
- Veja os logs do servidor no terminal
- Verifique se o bot já não está rodando

### Dashboard não carrega
- Verifique se o servidor Django está rodando
- Acesse http://localhost:8000 (não 127.0.0.1)
- Verifique se as migrações rodaram: `python manage.py migrate`

## 📚 Documentação Adicional

- **CLAUDE.md** - Documentação técnica completa
- **src/admin_dashboard/README.md** - Detalhes do Django
- **Discord.py docs** - https://discordpy.readthedocs.io/

## 🤝 Contribuindo

Este é um projeto pessoal, mas sugestões são bem-vindas!

## 📄 Licença

MIT License - Use como quiser!

---

**Desenvolvido com ❤️ usando:**
- Discord.py
- Django
- OpenRouter AI
- OpenAI Embeddings
- ChromaDB
