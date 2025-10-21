"""
Logging configuration for Discord Bot.
Provides structured logging with different levels and formats.
"""
import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from ..config.settings import settings


class DiscordBotLogger:
    """Centralized logging configuration for the Discord bot"""

    def __init__(self):
        self._logger: logging.Logger = logging.getLogger('discord_bot')
        self._setup_logger()

    def _setup_logger(self):
        """Setup logging configuration"""
        # Create logger
        self._logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

        # Remove existing handlers to avoid duplicates
        self._logger.handlers.clear()

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self._logger.addHandler(console_handler)

        # File handler for all logs
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / 'discord_bot.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        self._logger.addHandler(file_handler)

        # Error file handler
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / 'discord_bot_error.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        self._logger.addHandler(error_handler)

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Get logger instance"""
        if name:
            return self._logger.getChild(name)
        return self._logger

    def log_bot_event(self, event: str, user_id: Optional[str] = None, **kwargs):
        """Log bot-specific events"""
        extra = {'event_type': 'bot_event', 'event': event}
        if user_id:
            extra['user_id'] = user_id
        extra.update(kwargs)

        self._logger.info(f"Bot Event: {event}", extra=extra)

    def log_api_call(self, service: str, endpoint: str, success: bool, **kwargs):
        """Log API calls"""
        level = logging.INFO if success else logging.ERROR
        status = "SUCCESS" if success else "FAILED"

        extra = {
            'event_type': 'api_call',
            'service': service,
            'endpoint': endpoint,
            'success': success
        }
        extra.update(kwargs)

        self._logger.log(level, f"API Call: {service}.{endpoint} - {status}", extra=extra)

    def log_rag_operation(self, operation: str, success: bool, **kwargs):
        """Log RAG operations"""
        level = logging.INFO if success else logging.WARNING
        status = "SUCCESS" if success else "FAILED"

        extra = {
            'event_type': 'rag_operation',
            'operation': operation,
            'success': success
        }
        extra.update(kwargs)

        self._logger.log(level, f"RAG Operation: {operation} - {status}", extra=extra)

    def log_performance(self, operation: str, duration: float, **kwargs):
        """Log performance metrics"""
        extra = {
            'event_type': 'performance',
            'operation': operation,
            'duration_ms': duration
        }
        extra.update(kwargs)

        self._logger.info(f"Performance: {operation} took {duration:.2f}ms", extra=extra)

    def get_log_file_path(self) -> Path:
        """Get the path to the main log file"""
        return Path('logs') / 'discord_bot.log'

    def get_error_log_file_path(self) -> Path:
        """Get the path to the error log file"""
        return Path('logs') / 'discord_bot_error.log'


# Global logger instance
logger = DiscordBotLogger()