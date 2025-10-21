#!/usr/bin/env python3
"""
Main entry point for Discord Bot.
This file provides backward compatibility with the old structure.
"""
from src.discord_bot import DiscordBot


def main():
    """Run the Discord bot"""
    bot = DiscordBot()
    bot.run()


if __name__ == "__main__":
    main()
