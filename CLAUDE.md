# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Discord chatbot with conversational memory and RAG (Retrieval-Augmented Generation) capabilities. Uses OpenRouter for AI responses and OpenAI for document embeddings, with ChromaDB for vector storage and SQLite for conversation persistence.

## Project Structure

```
ChatBOT/
├── src/
│   ├── discord_bot/          # Discord bot package
│   │   ├── __init__.py
│   │   ├── bot/              # Discord bot logic
│   │   │   ├── client.py     # Main bot client and event handlers
│   │   │   ├── ai_client.py  # OpenRouter API integration
│   │   │   └── commands.py   # Command handlers
│   │   ├── database/         # Data persistence
│   │   │   └── sqlite_db.py  # SQLite database operations
│   │   ├── rag/              # RAG implementation
│   │   │   └── vector_store.py  # ChromaDB + OpenAI embeddings
│   │   ├── config/           # Configuration
│   │   │   └── settings.py   # Centralized settings management
│   │   └── utils/            # Utility functions
│   │       └── logging_config.py  # Logging configuration
│   └── admin_dashboard/      # Django admin dashboard
│       ├── settings.py       # Django settings
│       ├── urls.py           # Main URLs
│       ├── wsgi.py / asgi.py # WSGI/ASGI entry points
│       ├── manage.py         # Django CLI
│       └── admin_panel/      # Admin panel app
│           ├── views.py      # Views and API endpoints
│           ├── urls.py       # App URLs
│           ├── bot_manager.py  # Bot lifecycle manager
│           ├── templates/    # HTML templates
│           ├── static/       # CSS/JS files
│           └── management/   # Django commands
├── scripts/
│   └── import_documents.py   # Document import CLI tool
├── tests/                    # Test files (to be implemented)
├── docs/                     # Documentation
├── main.py                   # Entry point (bot + dashboard)
├── start_dashboard.sh        # Convenience startup script
└── pyproject.toml           # Poetry dependencies and config
```

## Architecture

### Core Components

**Bot Layer (`src/discord_bot/bot/`)**
- **client.py** - Main Discord client with event handlers
  - Handles mentions and DMs with conversational context
  - Routes commands to command_handler
  - Manages conversation flow with AI
  - Splits long messages for Discord's 2000-char limit

- **ai_client.py** - OpenRouter API client
  - Sends messages to AI with history and RAG context
  - Builds proper message format for OpenRouter
  - Handles errors and API responses

- **commands.py** - Command handler implementations
  - All bot commands (!ajuda, !limpar, !stats, etc.)
  - Separated from main client for better organization
  - Each command is a static method for easy testing

**Database Layer (`src/discord_bot/database/`)**
- **sqlite_db.py** - SQLite persistence
  - Schema: `users`, `messages`, `stats`
  - Conversation history is user-specific
  - All message operations update user stats atomically
  - Singleton pattern with `db` instance

**RAG Layer (`src/discord_bot/rag/`)**
- **vector_store.py** - ChromaDB vector database
  - Uses OpenAI API for embeddings (text-embedding-3-small)
  - All operations with embeddings are async
  - Collection name: "rag_collection" by default
  - Singleton pattern with `vector_store` instance

**Configuration (`src/discord_bot/config/`)**
- **settings.py** - Centralized configuration
  - All environment variables in one place
  - Validation of required settings
  - Constants for behavior (history limit, RAG results, etc.)
  - Singleton pattern with `settings` instance

### Data Flow

1. User mentions bot or sends DM → `client.py:on_message()`
2. Command routing in `client.py` → `commands.py` handlers
3. For conversations: `client._handle_conversation()`
   - Load last 10 messages from SQLite (`sqlite_db.py`)
   - Search ChromaDB for 2 relevant docs (`vector_store.py`)
   - Combine history + RAG context → send to OpenRouter (`ai_client.py`)
   - Save user message + bot response to SQLite
   - Update user stats atomically

## Development Commands

### Running the Bot with Admin Dashboard

```bash
# Start bot + admin dashboard (recommended)
python main.py

# Or use the convenience script
./start_dashboard.sh

# With Poetry
poetry run python main.py
```

**Access Dashboard:**
- URL: http://localhost:8000
- Default login: `admin` / `admin123`
- ⚠️ Change password after first login!

### Running Only the Bot (No Dashboard)

```bash
# Direct bot execution (legacy mode)
python -m src.discord_bot
```

### Document Import

```bash
# Import all PDFs/DOCXs from a directory
python scripts/import_documents.py ./documentos_exemplo
python scripts/import_documents.py /path/to/documents
```

### Dependencies

```bash
# Install dependencies via Poetry (recommended)
poetry install

# Activate virtual environment
poetry shell

# Run with poetry
poetry run python main.py

# Or manually install key packages:
pip install discord.py aiohttp chromadb openai pymupdf python-docx docx2txt
```

### Development Tools

```bash
# Code formatting with Black
black src/ scripts/

# Linting with Ruff
ruff check src/ scripts/

# Run tests (when implemented)
pytest tests/
```

## Environment Variables (Required)

- **TOKEN** - Discord bot token
- **OPENROUTER_API_KEY** - For AI chat responses
- **OPENAI_API_KEY** - For document embeddings (RAG)
- **EMBEDDING_MODEL** - (Optional) Defaults to "text-embedding-3-small"

## Key Implementation Details

### Singleton Pattern
The codebase uses singleton instances for core services:
- `settings` - Configuration (config/settings.py)
- `db` - SQLite database (database/sqlite_db.py)
- `vector_store` - ChromaDB vector store (rag/vector_store.py)
- `ai_client` - OpenRouter client (bot/ai_client.py)
- `command_handler` - Command handlers (bot/commands.py)

This ensures single initialization and shared state across the application.

### RAG Integration (bot/client.py:_handle_conversation)
```python
similar_docs = await vector_store.search_similar(user_message)
if similar_docs:
    rag_context = "\n\n".join([doc['text'] for doc in similar_docs])
```
RAG is **always** active when documents exist - no manual trigger needed. Number of results configured in `settings.RAG_SEARCH_RESULTS` (default: 2).

### Conversation History Management
- Stored in SQLite `messages` table with user_id, role, content, timestamp
- Retrieved in reverse chronological order, then reversed for proper context flow
- Limit: 10 messages per user (configurable via `settings.CONVERSATION_HISTORY_LIMIT`)
- DMs and mentions share the same conversation history per user

### Discord Message Splitting
Long AI responses (>2000 chars) are automatically chunked in `client._send_response()` to comply with Discord's message length limit (defined in `settings.DISCORD_MESSAGE_LIMIT`).

### Vector DB Async Pattern
All vector_store operations that involve embeddings are async because they call OpenAI API:
- `add_document()` - generates embedding before storing
- `search_similar()` - generates query embedding before search
- Non-async operations: `count_documents()`, `delete_all_documents()`, `list_collections()`

### Configuration Management
All settings are centralized in `config/settings.py`:
- Environment variables loaded via `os.getenv()`
- Default values provided for optional settings
- `settings.validate()` checks required variables
- `settings.get_system_prompt()` builds prompts with optional RAG context

## Database Schema

### SQLite (bot_data.db)
- **users**: user_id (PK), username, created_at
- **messages**: id (PK), user_id (FK), role, content, timestamp
- **stats**: user_id (PK, FK), message_count, last_interaction

### ChromaDB (./chroma_db/)
- **Collection**: "rag_collection"
- **Embeddings**: 1536-dimensional vectors (OpenAI text-embedding-3-small)
- **Metadata fields**: author, author_id, filename, filepath, filetype, imported_at, word_count, char_count

## Common Patterns

### Adding a New Command
1. Add handler method to `CommandHandler` class in `bot/commands.py`
   ```python
   @staticmethod
   async def handle_new_command(message: discord.Message, arg: str):
       # Implementation here
       await message.channel.send("Response")
   ```

2. Add routing in `bot/client.py:on_message()`
   ```python
   if user_message.lower().startswith('!newcommand '):
       arg = user_message[12:].strip()
       await command_handler.handle_new_command(message, arg)
       return
   ```

3. Update help text in `bot/commands.py:handle_help()`

### Modifying AI Behavior
- System prompt: `config/settings.py:SYSTEM_PROMPT`
- RAG context injection: `config/settings.py:get_system_prompt()`
- Model selection: `config/settings.py:OPENROUTER_MODEL` or set `OPENROUTER_MODEL` env var
- See OpenRouter docs for available models: https://openrouter.ai/models

### Adding New Configuration
1. Add setting to `config/settings.py:Settings` class
   ```python
   NEW_SETTING: str = os.getenv("NEW_SETTING", "default_value")
   ```

2. If required, add validation in `settings.validate()`
   ```python
   if not cls.NEW_SETTING:
       errors.append("NEW_SETTING environment variable is required")
   ```

3. Import and use: `from src.discord_bot.config import settings`

## Admin Dashboard

### Overview
The project includes a Django-based admin dashboard for managing the Discord bot without command-line access. The dashboard provides:

**Features:**
- ✅ Bot Control: Start, stop, restart bot with web UI
- ✅ Real-time Monitoring: Status, uptime, system metrics (CPU, memory)
- ✅ Statistics: User count, message count, bot activity
- ✅ Logs Viewer: Real-time log streaming and export (TXT/JSON)
- ✅ RAG Management: Upload documents, process embeddings, view stats
- ✅ Authentication: Secure login with Django Auth

### Dashboard Structure

**Location:** `src/admin_dashboard/`

**Key Files:**
- `settings.py` - Django configuration
- `admin_panel/views.py` - API endpoints and page views
- `admin_panel/bot_manager.py` - Bot lifecycle manager (singleton)
- `admin_panel/templates/` - HTML templates (Jinja2)
- `admin_panel/static/` - CSS and JavaScript

### Bot Control via Dashboard

The `bot_manager.py` module provides a singleton to control the bot:

```python
from admin_dashboard.admin_panel.bot_manager import bot_manager

# Start bot
bot_manager.start_bot()  # Returns {"success": True/False, "message": "..."}

# Stop bot
bot_manager.stop_bot()

# Restart bot
bot_manager.restart_bot()

# Get status
status = bot_manager.get_status()
# Returns: {"is_running": bool, "uptime": str, "start_time": ISO timestamp}
```

**Important:** The bot is NOT auto-started when `main.py` runs. It must be started from the dashboard or programmatically.

### API Endpoints

**Bot Control:**
- `POST /api/bot/start` - Start bot
- `POST /api/bot/stop` - Stop bot
- `POST /api/bot/restart` - Restart bot
- `GET /api/bot/status` - Get status

**Monitoring:**
- `GET /api/stats` - Bot and system statistics
- `GET /api/uptime` - Uptime in seconds
- `GET /api/logs/stream` - Server-Sent Events log stream
- `GET /api/logs/export?format=txt|json` - Download logs

**Embeddings:**
- `GET /api/embeddings/stats` - RAG collection stats
- `POST /api/embeddings/process` - Upload and process document
- `DELETE /api/embeddings/clear` - Clear all embeddings

### Dashboard Management Commands

```bash
# Create admin user
cd src/admin_dashboard
python manage.py create_admin --username admin --password secret

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run dashboard standalone (without bot)
python manage.py runserver
```

### Dashboard Security

- Authentication required for all pages and APIs
- CSRF protection on POST requests
- Default bind to localhost only (127.0.0.1)
- Separate database from bot data (`admin_dashboard.db` vs `bot_data.db`)
- Django session management with secure cookies

## Testing

### Manual Testing
No automated test suite currently exists. Manual testing via Discord:
1. Test conversation memory: Send multiple messages, verify context retention
2. Test RAG: Add document with !adicionar, ask related question
3. Test commands: !stats, !rag_stats, !limpar, etc.
4. Test document import: Run `python scripts/import_documents.py` on test directory

**Dashboard Testing:**
1. Access http://localhost:8000 and login
2. Test bot controls (start/stop/restart)
3. Monitor real-time stats and uptime
4. View and export logs
5. Upload test document and verify embedding processing

### Future Testing Strategy
When implementing tests (in `tests/` directory):
- Unit tests for individual modules (`test_sqlite_db.py`, `test_vector_store.py`, etc.)
- Integration tests for bot commands (`test_commands.py`)
- Mock Discord messages and OpenAI/OpenRouter APIs
- Use pytest fixtures for database and vector store setup/teardown
- Dashboard tests: Test API endpoints, authentication, bot manager

## Troubleshooting

### Bot doesn't respond
- Verify MESSAGE CONTENT INTENT enabled in Discord Developer Portal
- Check TOKEN and API keys are set correctly
- Confirm bot has Send Messages permission in server

### RAG not working
- Verify OPENAI_API_KEY is set and has credits
- Check ChromaDB initialized: vector_db.init_vector_db() called at startup
- Verify documents exist: Use !rag_stats command

### Embeddings failing
- OpenAI account needs minimum $5 credits
- text-embedding-3-small costs ~$0.02 per 1M tokens (very cheap)
- Check API key has embeddings permission (not just chat)

### Dashboard not accessible
- Ensure Django server is running (check terminal output)
- Verify accessing http://localhost:8000 (not 127.0.0.1)
- Check firewall settings if running remotely
- Verify migrations ran successfully: `python manage.py migrate`

### Bot won't start from dashboard
- Check Discord TOKEN is set in environment variables
- Verify bot initialization completed (check server logs)
- Ensure bot isn't already running (check status)
- Check logs for detailed error messages
