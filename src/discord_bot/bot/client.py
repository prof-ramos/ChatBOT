"""
Discord bot client and event handlers.
"""
import discord
import time

from ..config.settings import settings
from ..database.sqlite_db import db
# from ..rag.vector_store import vector_store  # Temporarily disabled due to ChromaDB dependency issues
from .ai_client import ai_client
from .commands import command_handler
from ..utils.logging_config import logger as bot_logger


class DiscordBot:
    """Main Discord bot class"""

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = False
        intents.presences = False

        self.client = discord.Client(intents=intents)
        self._setup_events()

    def _setup_events(self):
        """Setup Discord event handlers"""

        @self.client.event
        async def on_ready():
            """Handle bot ready event"""
            start_time = time.time()
            bot_logger.get_logger().info("Initializing bot components...")

            try:
                db.init_database()
                bot_logger.log_bot_event("database_initialized", success=True)
            except Exception as e:
                bot_logger.get_logger().error(f"Failed to initialize database: {e}")
                return

            # vector_store.init_vector_db()  # Temporarily disabled
            bot_logger.get_logger().warning("RAG system temporarily disabled due to ChromaDB dependency issues")

            init_time = time.time() - start_time
            bot_logger.log_performance("bot_initialization", init_time * 1000)

            bot_logger.get_logger().info(f'Bot connected as {self.client.user} (ID: {self.client.user.id})')
            bot_logger.log_bot_event("bot_ready", user_id=str(self.client.user.id))

        @self.client.event
        async def on_message(message):
            """Handle incoming messages"""
            start_time = time.time()

            # Ignore bot's own messages
            if message.author == self.client.user:
                return

            user_id = str(message.author.id)
            username = str(message.author)
            channel_type = "DM" if isinstance(message.channel, discord.DMChannel) else "channel"

            bot_logger.log_bot_event("message_received",
                               user_id=user_id,
                               username=username,
                               channel_type=channel_type,
                               message_length=len(message.content))

            # Check if message is DM or mentions bot
            is_dm = isinstance(message.channel, discord.DMChannel)
            is_mentioned = self.client.user in message.mentions

            if not (is_dm or is_mentioned):
                bot_logger.get_logger().debug(f"Ignoring message from {username} - not DM or mention")
                return

            # Clean message content
            user_message = message.content.replace(
                f'<@{self.client.user.id}>', ''
            ).replace(
                f'<@!{self.client.user.id}>', ''
            ).strip()

            user_id = str(message.author.id)
            username = str(message.author)

            # Handle commands
            if user_message.lower() == '!ajuda':
                await command_handler.handle_help(message)
                return

            if user_message.lower() == '!limpar':
                await command_handler.handle_clear_history(message)
                return

            if user_message.lower() == '!stats':
                await command_handler.handle_stats(message)
                return

            if user_message.lower() == '!stats_global':
                await command_handler.handle_global_stats(message)
                return

            if user_message.lower().startswith('!adicionar '):
                doc_text = user_message[11:].strip()
                await command_handler.handle_add_document(message, doc_text)
                return

            if user_message.lower().startswith('!buscar '):
                query = user_message[8:].strip()
                await command_handler.handle_search_documents(message, query)
                return

            if user_message.lower() == '!rag_stats':
                await command_handler.handle_rag_stats(message)
                return

            if user_message.lower() == '!limpar_rag':
                await command_handler.handle_clear_rag(message)
                return

            # Handle conversational messages
            await self._handle_conversation(message, user_id, username, user_message)

    async def _handle_conversation(
        self,
        message: discord.Message,
        user_id: str,
        username: str,
        user_message: str
    ):
        """Handle conversational messages with AI"""
        # Add/update user
        db.add_user(user_id, username)

        # Get conversation history
        history = db.get_conversation_history(user_id)

        # Search for relevant documents (RAG) - Temporarily disabled
        rag_context = None
        # similar_docs = await vector_store.search_similar(user_message)
        # if similar_docs:
        #     rag_context = "\n\n".join([doc['text'] for doc in similar_docs])

        # Save user message
        db.save_message(user_id, "user", user_message)

        # Get AI response
        async with message.channel.typing():
            ai_response = await ai_client.get_response(
                user_message,
                history,
                rag_context
            )

            # Save assistant response
            db.save_message(user_id, "assistant", ai_response)

            # Send response (split if too long)
            await self._send_response(message.channel, ai_response)

    async def _send_response(self, channel, response: str):
        """Send response to Discord, splitting if necessary"""
        if len(response) > settings.DISCORD_MESSAGE_LIMIT:
            chunks = [
                response[i:i + settings.DISCORD_MESSAGE_LIMIT]
                for i in range(0, len(response), settings.DISCORD_MESSAGE_LIMIT)
            ]
            for chunk in chunks:
                await channel.send(chunk)
        else:
            await channel.send(response)

    def run(self, token: str = None):
        """Run the Discord bot"""
        token = token or settings.DISCORD_TOKEN

        if not token:
            raise ValueError("Discord token is required. Set TOKEN environment variable.")

        # Validate settings
        errors = settings.validate()
        if errors:
            raise ValueError(f"Configuration errors:\n" + "\n".join(f"- {e}" for e in errors))

        try:
            self.client.run(token)
        except discord.HTTPException as e:
            if e.status == 429:
                print("The Discord servers denied the connection for making too many requests")
                print("Get help from https://stackoverflow.com/questions/66724687/")
            else:
                raise e
