# Migration Guide: v1 to v2

## Overview

O projeto foi reorganizado seguindo as melhores práticas de estrutura Python, com separação clara de responsabilidades e melhor organização do código.

## Estrutura Antiga vs Nova

### Antes (v1)
```
ChatBOT/
├── main.py          # Tudo em um arquivo
├── database.py      # Funções de banco de dados
├── vector_db.py     # Funções RAG
└── import_documents.py
```

### Depois (v2)
```
ChatBOT/
├── src/
│   └── discord_bot/
│       ├── bot/              # Lógica do bot
│       ├── database/         # Persistência
│       ├── rag/              # RAG/embeddings
│       ├── config/           # Configuração
│       └── utils/            # Utilitários
├── scripts/
│   └── import_documents.py
├── tests/                    # Testes (futuro)
└── main.py                   # Entry point
```

## Principais Mudanças

### 1. Separação de Responsabilidades

**Bot Layer**
- `bot/client.py` - Cliente Discord e event handlers
- `bot/ai_client.py` - Integração com OpenRouter
- `bot/commands.py` - Handlers de comandos

**Database Layer**
- `database/sqlite_db.py` - Operações SQLite (antes: `database.py`)

**RAG Layer**
- `rag/vector_store.py` - ChromaDB + embeddings (antes: `vector_db.py`)

**Configuration**
- `config/settings.py` - Configuração centralizada (NOVO)

### 2. Padrão Singleton

Todas as instâncias principais são singletons:
```python
from src.discord_bot.config import settings
from src.discord_bot.database import db
from src.discord_bot.rag import vector_store
from src.discord_bot.bot import ai_client
```

### 3. Configuração Centralizada

Antes:
```python
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or ""
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
```

Depois:
```python
from src.discord_bot.config import settings

settings.OPENROUTER_API_KEY
settings.OPENROUTER_BASE_URL
settings.validate()  # Valida configurações
```

## Como Migrar Código Existente

### Importações

**Antes:**
```python
import database
import vector_db

database.save_message(user_id, "user", text)
doc_id = await vector_db.add_document(text)
```

**Depois:**
```python
from src.discord_bot.database import db
from src.discord_bot.rag import vector_store

db.save_message(user_id, "user", text)
doc_id = await vector_store.add_document(text)
```

### Comandos

**Antes:** Tudo em `main.py:on_message()`

**Depois:** Cada comando tem seu handler em `bot/commands.py`
```python
from src.discord_bot.bot.commands import command_handler

await command_handler.handle_stats(message)
```

### Configurações

**Antes:** Espalhadas pelo código

**Depois:** Centralizadas em `config/settings.py`
```python
from src.discord_bot.config import settings

# Acesso
settings.CONVERSATION_HISTORY_LIMIT
settings.RAG_SEARCH_RESULTS

# Validação
errors = settings.validate()
```

## Execução

### Nada muda para o usuário final!

```bash
# Continua funcionando normalmente
python main.py

# Importação de documentos
python scripts/import_documents.py ./docs

# Com Poetry
poetry install
poetry run python main.py
```

## Benefícios

1. **Organização** - Código mais limpo e fácil de navegar
2. **Manutenibilidade** - Módulos independentes e testáveis
3. **Escalabilidade** - Fácil adicionar novas funcionalidades
4. **Testabilidade** - Estrutura preparada para testes unitários
5. **Configurabilidade** - Settings centralizados e validados
6. **Padrões Python** - Segue convenções da comunidade

## Arquivos Antigos

Os arquivos antigos (`database.py`, `vector_db.py`, `import_documents.py` na raiz) podem ser removidos após confirmar que o novo código funciona corretamente.

**IMPORTANTE:** Faça backup do banco de dados antes:
```bash
cp bot_data.db bot_data.db.backup
cp -r chroma_db/ chroma_db.backup/
```

## Próximos Passos

1. ✅ Estrutura reorganizada
2. ✅ Configuração centralizada
3. ✅ Singleton pattern implementado
4. ⏳ Implementar testes unitários
5. ⏳ Adicionar logging estruturado
6. ⏳ Documentação de API
