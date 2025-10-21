#!/usr/bin/env python3
"""
Main entry point for Discord Bot with Admin Dashboard.
Runs both the Discord bot and Django admin panel in a single process.
"""
import os
import sys
import threading
import time
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_dashboard.settings')


def run_discord_bot():
    """Run Discord bot in background thread"""
    from discord_bot import DiscordBot
    from admin_dashboard.admin_panel.bot_manager import bot_manager

    print("🤖 Initializing Discord bot...")
    bot = DiscordBot()

    # Register bot with manager
    bot_manager.set_bot(bot)

    # Note: Bot won't auto-start, must be started from dashboard
    print("✅ Discord bot initialized (use dashboard to start)")

    # Keep thread alive
    while True:
        time.sleep(1)


def run_django_server():
    """Run Django development server"""
    import django
    from django.core.management import execute_from_command_line

    print("🌐 Starting Django admin dashboard...")

    # Setup Django
    django.setup()

    # Run migrations
    print("📦 Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])

    # Collect static files
    print("📁 Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

    # Create default admin user if needed
    print("👤 Creating default admin user...")
    execute_from_command_line(['manage.py', 'create_admin'])

    # Start server
    print("\n" + "="*60)
    print("✅ Discord Bot Admin Dashboard")
    print("="*60)
    print("📍 Dashboard URL: http://localhost:8000")
    print("👤 Default login: admin / admin123")
    print("🔧 Change password after first login!")
    print("="*60 + "\n")

    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])


def main():
    """Main entry point"""
    print("\n🚀 Starting Discord Bot with Admin Dashboard...\n")

    # Start Discord bot in background thread
    bot_thread = threading.Thread(target=run_discord_bot, daemon=True)
    bot_thread.start()

    # Give bot time to initialize
    time.sleep(2)

    # Run Django server in main thread
    try:
        run_django_server()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
