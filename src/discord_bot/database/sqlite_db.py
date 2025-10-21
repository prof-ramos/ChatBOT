"""
SQLite database management for conversation history and user statistics.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

from ..config.settings import settings


class SQLiteDatabase:
    """SQLite database manager for bot data"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.SQLITE_DB_PATH

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """Initialize the database and create necessary tables"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Stats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                user_id TEXT PRIMARY KEY,
                message_count INTEGER DEFAULT 0,
                last_interaction TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        conn.commit()
        conn.close()
        print(f"✅ SQLite database initialized: {self.db_path}")

    def add_user(self, user_id: str, username: str):
        """Add or update a user in the database"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users (user_id, username)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET username = excluded.username
            """, (user_id, username))

            cursor.execute("""
                INSERT OR IGNORE INTO stats (user_id, message_count, last_interaction)
                VALUES (?, 0, ?)
            """, (user_id, datetime.now()))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error adding user {user_id}: {e}")
            if conn:
                conn.close()

    def save_message(self, user_id: str, role: str, content: str):
        """Save a message to the conversation history"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages (user_id, role, content)
            VALUES (?, ?, ?)
        """, (user_id, role, content))

        cursor.execute("""
            UPDATE stats
            SET message_count = message_count + 1,
                last_interaction = ?
            WHERE user_id = ?
        """, (datetime.now(), user_id))

        conn.commit()
        conn.close()

    def get_conversation_history(self, user_id: str, limit: int = None) -> List[Dict[str, str]]:
        """Get conversation history for a user"""
        if limit is None:
            limit = settings.CONVERSATION_HISTORY_LIMIT

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT role, content
            FROM messages
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))

        messages = cursor.fetchall()
        conn.close()

        # Reverse to get chronological order
        history = []
        for role, content in reversed(messages):
            history.append({"role": role, "content": content})

        return history

    def clear_user_history(self, user_id: str):
        """Clear conversation history for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
        cursor.execute("""
            UPDATE stats
            SET message_count = 0
            WHERE user_id = ?
        """, (user_id,))

        conn.commit()
        conn.close()

    def get_user_stats(self, user_id: str) -> Optional[Dict]:
        """Get statistics for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.username, s.message_count, s.last_interaction
            FROM users u
            LEFT JOIN stats s ON u.user_id = s.user_id
            WHERE u.user_id = ?
        """, (user_id,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                "username": result[0],
                "message_count": result[1] or 0,
                "last_interaction": result[2]
            }
        return None

    def get_total_stats(self) -> Dict:
        """Get global bot statistics"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM messages")
        total_messages = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM messages WHERE role = 'user'")
        user_messages = cursor.fetchone()[0]

        conn.close()

        return {
            "total_users": total_users,
            "total_messages": total_messages,
            "user_messages": user_messages,
            "bot_responses": total_messages - user_messages
        }


# Singleton instance
db = SQLiteDatabase()
