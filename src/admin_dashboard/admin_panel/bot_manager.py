"""
Bot manager singleton to control the Discord bot from Django.
"""
import asyncio
import threading
import time
from datetime import datetime
from typing import Optional


class BotManager:
    """Singleton manager for Discord bot lifecycle"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.bot = None
        self.bot_thread = None
        self.is_running = False
        self.start_time = None
        self.stop_event = threading.Event()
        self._initialized = True

    def set_bot(self, bot):
        """Set the Discord bot instance"""
        self.bot = bot

    def start_bot(self):
        """Start the Discord bot in a separate thread"""
        if self.is_running:
            return {"success": False, "message": "Bot já está rodando"}

        if not self.bot:
            return {"success": False, "message": "Bot não inicializado"}

        try:
            self.stop_event.clear()
            self.bot_thread = threading.Thread(target=self._run_bot, daemon=True)
            self.bot_thread.start()
            self.is_running = True
            self.start_time = datetime.now()

            # Wait a bit to ensure bot starts properly
            time.sleep(2)

            return {"success": True, "message": "Bot iniciado com sucesso"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao iniciar bot: {str(e)}"}

    def stop_bot(self):
        """Stop the Discord bot gracefully"""
        if not self.is_running:
            return {"success": False, "message": "Bot não está rodando"}

        try:
            # Signal bot to stop
            self.stop_event.set()

            # Close the bot connection
            if self.bot and self.bot.client:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.bot.client.close())
                loop.close()

            # Wait for thread to finish
            if self.bot_thread:
                self.bot_thread.join(timeout=5)

            self.is_running = False
            self.start_time = None

            return {"success": True, "message": "Bot parado com sucesso"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao parar bot: {str(e)}"}

    def restart_bot(self):
        """Restart the Discord bot"""
        stop_result = self.stop_bot()
        if not stop_result["success"]:
            return stop_result

        # Wait a bit before restarting
        time.sleep(2)

        return self.start_bot()

    def _run_bot(self):
        """Internal method to run bot in thread"""
        try:
            from discord_bot.config.settings import settings
            self.bot.run(settings.DISCORD_TOKEN)
        except Exception as e:
            print(f"Error running bot: {e}")
            self.is_running = False

    def get_status(self):
        """Get bot status information"""
        uptime = None
        if self.is_running and self.start_time:
            delta = datetime.now() - self.start_time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime = f"{hours}h {minutes}m {seconds}s"

        return {
            "is_running": self.is_running,
            "uptime": uptime,
            "start_time": self.start_time.isoformat() if self.start_time else None,
        }

    def get_uptime_seconds(self) -> Optional[int]:
        """Get uptime in seconds"""
        if self.is_running and self.start_time:
            delta = datetime.now() - self.start_time
            return int(delta.total_seconds())
        return None


# Singleton instance
bot_manager = BotManager()
