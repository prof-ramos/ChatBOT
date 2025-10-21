"""
AI client for OpenRouter API interactions.
"""
from typing import List, Dict, Optional

import aiohttp

from ..config.settings import settings


class AIClient:
    """Client for interacting with OpenRouter API"""

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or settings.OPENROUTER_API_KEY
        self.base_url = base_url or settings.OPENROUTER_BASE_URL
        self.model = model or settings.OPENROUTER_MODEL

    async def get_response(
        self,
        user_message: str,
        conversation_history: List[Dict] = None,
        rag_context: Optional[str] = None
    ) -> str:
        """
        Get AI response from OpenRouter.

        Args:
            user_message: The user's current message
            conversation_history: List of previous messages
            rag_context: Optional context from RAG search

        Returns:
            AI response text
        """
        if not self.api_key:
            return "Error: OPENROUTER_API_KEY not configured. Please add the key to environment variables."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Build system message
        system_message = settings.get_system_prompt(rag_context)

        # Build messages array
        messages = [{"role": "system", "content": system_message}]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": user_message})

        # Build payload
        payload = {
            "model": self.model,
            "messages": messages
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        return f"Error connecting to AI (status {response.status}): {error_text}"
        except Exception as e:
            return f"Error processing your message: {str(e)}"


# Singleton instance
ai_client = AIClient()
