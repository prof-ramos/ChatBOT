# Overview

A Discord chatbot application that leverages AI models through the OpenRouter API to provide intelligent responses with RAG (Retrieval-Augmented Generation) capabilities. The bot activates when mentioned in Discord servers or receives direct messages, using OpenRouter's access to 400+ AI models to generate Portuguese-language responses enriched with relevant document context from a vector database.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Application Type
Single-file Python application using Discord.py library with async/await patterns for event-driven bot interactions.

## Core Components

### Discord Integration
- **Library**: discord.py with async client pattern
- **Intents Configuration**: Uses default intents with message_content enabled, members and presences disabled
- **Event Model**: Event-driven architecture responding to Discord events (mentions and direct messages)
- **Rationale**: Discord.py provides robust async support and simplified API interaction, while selective intent usage minimizes overhead and privacy concerns

### AI Response System
- **Provider**: OpenRouter API (https://openrouter.ai)
- **Model**: meta-llama/llama-3.1-8b-instruct:free (configurable)
- **Communication**: Async HTTP requests using aiohttp
- **System Prompt**: Portuguese-language friendly assistant persona
- **Rationale**: OpenRouter provides access to multiple AI models through a single API, with the free Llama model offering cost-effective responses. Async HTTP ensures non-blocking operations during AI processing

### Message Handling
- **Response Triggering**: Bot mentions in servers and direct messages
- **User Feedback**: "Typing..." indicator during AI processing
- **Long Message Handling**: Automatic message splitting for responses exceeding Discord's 2000-character limit
- **Rationale**: Clear user feedback improves UX, while automatic message splitting ensures complete response delivery

## Configuration Management
- **Environment Variables**: Secrets-based configuration for sensitive credentials
  - `TOKEN`: Discord bot authentication token
  - `OPENROUTER_API_KEY`: OpenRouter API authentication key
- **Rationale**: Environment-based configuration separates credentials from code and enables secure deployment on Replit

## Error Handling
- **API Key Validation**: Checks for OPENROUTER_API_KEY presence before making requests
- **HTTP Status Handling**: Returns detailed error messages including status codes and response text
- **Rationale**: Graceful degradation with informative error messages aids debugging and user awareness

# External Dependencies

## Third-Party Services

### Discord Platform
- **Purpose**: Bot hosting and message delivery
- **Authentication**: Bot token from Discord Developer Portal
- **Required Permissions**: Send Messages, Read Message History, Read Messages/View Channels
- **Gateway Intents**: MESSAGE CONTENT INTENT (required), SERVER MEMBERS INTENT (optional)

### OpenRouter API
- **Purpose**: AI model access and response generation
- **Endpoint**: https://openrouter.ai/api/v1/chat/completions
- **Authentication**: Bearer token (API key)
- **Current Model**: meta-llama/llama-3.1-8b-instruct:free
- **Model Access**: 400+ available AI models through unified API

### OpenAI API
- **Purpose**: Text embeddings for RAG system
- **Endpoint**: https://api.openai.com/v1/embeddings
- **Authentication**: Bearer token (API key)
- **Current Model**: text-embedding-3-small
- **Cost**: ~$0.02 per 1M tokens
- **Usage**: Converting documents to vector representations for semantic search

## Python Libraries
- **discord.py**: Discord API wrapper for bot functionality
- **openai**: OpenAI API client for embeddings
- **chromadb**: Vector database for document storage and similarity search
- **pymupdf**: PDF text extraction
- **python-docx**: DOCX document processing
- **docx2txt**: Alternative DOCX/DOC text extraction

## Deployment Platform
- **Replit**: Hosting environment with integrated secrets management
- **Configuration Method**: Replit Secrets for TOKEN, OPENROUTER_API_KEY, and OPENAI_API_KEY storage