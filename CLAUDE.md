# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Discord chatbot with conversational memory and RAG (Retrieval-Augmented Generation) capabilities. Uses OpenRouter for AI responses and OpenAI for document embeddings, with ChromaDB for vector storage and SQLite for conversation persistence.

## Architecture

### Core Components

- **main.py** - Discord bot entry point and message handling logic
  - Handles mentions and DMs with conversational context
  - Integrates RAG: automatically searches top 2 relevant docs per query
  - Routes commands (!ajuda, !limpar, !stats, !adicionar, !buscar, etc.)
  - Maintains 10-message conversation history per user via database.py

- **database.py** - SQLite persistence layer
  - Schema: `users`, `messages`, `stats`
  - Conversation history is user-specific (DMs and mentions share same history)
  - All message operations update user stats atomically

- **vector_db.py** - ChromaDB vector database interface
  - Uses OpenAI API for embeddings (text-embedding-3-small model)
  - All operations are async due to embedding API calls
  - Collection name: "rag_collection" by default
  - Stores embeddings + metadata (author, timestamps, etc.)

- **import_documents.py** - Bulk document import CLI tool
  - Supports PDF (PyMuPDF), DOCX, DOC formats
  - Extracts text, generates embeddings, stores in ChromaDB
  - Usage: `python import_documents.py <directory>`

### Data Flow

1. User mentions bot or sends DM → main.py:on_message()
2. Load last 10 messages from SQLite (database.py)
3. Search ChromaDB for 2 most relevant docs (vector_db.py)
4. Combine history + RAG context → send to OpenRouter API
5. Save user message + bot response to SQLite
6. Update user stats (message count, last_interaction)

## Development Commands

### Running the Bot

```bash
# Start the bot (requires environment variables)
python main.py
```

### Document Import

```bash
# Import all PDFs/DOCXs from a directory
python import_documents.py ./documentos_exemplo
python import_documents.py /path/to/documents
```

### Dependencies

```bash
# Install dependencies via Poetry
poetry install

# Or manually install key packages:
pip install discord.py aiohttp chromadb openai pymupdf python-docx docx2txt
```

## Environment Variables (Required)

- **TOKEN** - Discord bot token
- **OPENROUTER_API_KEY** - For AI chat responses
- **OPENAI_API_KEY** - For document embeddings (RAG)
- **EMBEDDING_MODEL** - (Optional) Defaults to "text-embedding-3-small"

## Key Implementation Details

### RAG Integration (main.py:203-206)
```python
similar_docs = await vector_db.search_similar(user_message, n_results=2)
if similar_docs:
    rag_context = "\n\n".join([doc['text'] for doc in similar_docs])
```
RAG is **always** active when documents exist - no manual trigger needed.

### Conversation History Management
- Stored in SQLite `messages` table with user_id, role, content, timestamp
- Retrieved in reverse chronological order, then reversed for proper context flow
- Limit: 10 messages per user (configurable via database.py:get_conversation_history)

### Discord Message Splitting
Long AI responses (>2000 chars) are automatically chunked at main.py:215-220 to comply with Discord's message length limit.

### Vector DB Async Pattern
All vector_db operations that involve embeddings are async because they call OpenAI API:
- `add_document()` - generates embedding before storing
- `search_similar()` - generates query embedding before search
- Non-async operations: `count_documents()`, `delete_all_documents()`, `list_collections()`

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
1. Check for command prefix in main.py:on_message()
2. Extract command arguments via string slicing
3. Perform operation (DB query, vector search, etc.)
4. Send response via `await message.channel.send()`
5. Add to help text in !ajuda command (main.py:173-196)

### Modifying AI Behavior
- System prompt: main.py:28-31
- RAG context injection: main.py:30-31
- Model selection: main.py:49 (change "meta-llama/llama-3.1-8b-instruct:free")
- See OpenRouter docs for available models: https://openrouter.ai/models

## Testing

No automated test suite currently exists. Manual testing via Discord:
1. Test conversation memory: Send multiple messages, verify context retention
2. Test RAG: Add document with !adicionar, ask related question
3. Test commands: !stats, !rag_stats, !limpar, etc.
4. Test document import: Run import_documents.py on test directory

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
