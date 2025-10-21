"""
Configuration settings for Discord Bot.
Loads environment variables and provides centralized configuration.
"""
import os
from typing import Optional


class Settings:
    """Bot configuration settings"""

    # Discord Configuration
    DISCORD_TOKEN: str = os.getenv("TOKEN", "")

    # OpenRouter Configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1/chat/completions"
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")

    # OpenAI Configuration (for embeddings)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Database Configuration
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "bot_data.db")
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    CHROMA_COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "rag_collection")

    # Bot Behavior Configuration
    CONVERSATION_HISTORY_LIMIT: int = int(os.getenv("CONVERSATION_HISTORY_LIMIT", "10"))
    RAG_SEARCH_RESULTS: int = int(os.getenv("RAG_SEARCH_RESULTS", "2"))
    DISCORD_MESSAGE_LIMIT: int = 2000  # Discord's message length limit

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # System Prompt
    SYSTEM_PROMPT: str = (
        "Você é um assistente útil e amigável que responde em português. "
        "Você mantém o contexto das conversas anteriores."
    )

    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration settings"""
        errors = []

        if not cls.DISCORD_TOKEN:
            errors.append("TOKEN environment variable is required")

        if not cls.OPENROUTER_API_KEY:
            errors.append("OPENROUTER_API_KEY environment variable is required")

        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY environment variable is required for embeddings")

        return errors

    @classmethod
    def get_system_prompt(cls, rag_context: Optional[str] = None) -> str:
        """Get system prompt with optional RAG context"""
        prompt = cls.SYSTEM_PROMPT

        if rag_context:
            prompt += f"\n\nContexto relevante da base de conhecimento:\n{rag_context}"

        return prompt


settings = Settings()
