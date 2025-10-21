import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = "bot_data.db"

def init_database():
    """Inicializa o banco de dados e cria as tabelas necessárias"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
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
    print(f"✅ Banco de dados inicializado: {DB_PATH}")


def add_user(user_id: str, username: str):
    """Adiciona ou atualiza um usuário no banco de dados"""
    try:
        conn = sqlite3.connect(DB_PATH)
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
        print(f"Erro ao adicionar usuário {user_id}: {e}")
        if conn:
            conn.close()


def save_message(user_id: str, role: str, content: str):
    """Salva uma mensagem no histórico"""
    conn = sqlite3.connect(DB_PATH)
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


def get_conversation_history(user_id: str, limit: int = 10) -> List[Dict[str, str]]:
    """Retorna o histórico de conversas de um usuário"""
    conn = sqlite3.connect(DB_PATH)
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
    
    history = []
    for role, content in reversed(messages):
        history.append({"role": role, "content": content})
    
    return history


def clear_user_history(user_id: str):
    """Limpa o histórico de conversas de um usuário"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
    cursor.execute("""
        UPDATE stats
        SET message_count = 0
        WHERE user_id = ?
    """, (user_id,))
    
    conn.commit()
    conn.close()


def get_user_stats(user_id: str) -> Optional[Dict]:
    """Retorna estatísticas de um usuário"""
    conn = sqlite3.connect(DB_PATH)
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


def get_total_stats() -> Dict:
    """Retorna estatísticas globais do bot"""
    conn = sqlite3.connect(DB_PATH)
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
