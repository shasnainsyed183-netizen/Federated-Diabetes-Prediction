"""
MediFederate Chat History Database
Persistent storage for chat sessions and messages
"""

import sqlite3
import json
from datetime import datetime
import uuid


DB_PATH = 'chat_history.db'


def _get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_chat_db():
    """Create tables if not exists"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        
        # Chats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id TEXT PRIMARY KEY,
                user_email TEXT NOT NULL,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (chat_id) REFERENCES chats(id)
            )
        ''')
        
        conn.commit()
    finally:
        conn.close()


def create_chat(user_email, title="New Chat"):
    """Create a new chat session"""
    chat_id = str(uuid.uuid4())[:12]
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chats (id, user_email, title, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, user_email, title, now, now))
        conn.commit()
        return chat_id
    finally:
        conn.close()


def get_user_chats(user_email):
    """Get all chats for a user (newest first)"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, created_at, updated_at
            FROM chats
            WHERE user_email = ?
            ORDER BY updated_at DESC
        ''', (user_email,))
        rows = cursor.fetchall()
        return [
            {
                'id': r[0],
                'title': r[1],
                'created_at': r[2],
                'updated_at': r[3]
            }
            for r in rows
        ]
    finally:
        conn.close()


def get_chat_messages(chat_id):
    """Get all messages for a chat"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT role, content, timestamp
            FROM messages
            WHERE chat_id = ?
            ORDER BY id ASC
        ''', (chat_id,))
        rows = cursor.fetchall()
        return [
            {
                'role': r[0],
                'content': r[1],
                'timestamp': r[2]
            }
            for r in rows
        ]
    finally:
        conn.close()


def add_message(chat_id, role, content):
    """Add a message to a chat"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (chat_id, role, content, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, role, content, now))
        
        # Update chat's updated_at
        cursor.execute('''
            UPDATE chats SET updated_at = ? WHERE id = ?
        ''', (now, chat_id))
        
        conn.commit()
    finally:
        conn.close()


def update_chat_title(chat_id, new_title):
    """Update chat title"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE chats SET title = ? WHERE id = ?
        ''', (new_title, chat_id))
        conn.commit()
    finally:
        conn.close()


def delete_chat(chat_id):
    """Delete a chat and its messages"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages WHERE chat_id = ?', (chat_id,))
        cursor.execute('DELETE FROM chats WHERE id = ?', (chat_id,))
        conn.commit()
    finally:
        conn.close()


def clear_user_chats(user_email):
    """Delete all chats for a user"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM messages WHERE chat_id IN (
                SELECT id FROM chats WHERE user_email = ?
            )
        ''', (user_email,))
        cursor.execute('DELETE FROM chats WHERE user_email = ?', (user_email,))
        conn.commit()
    finally:
        conn.close()


def chat_count(user_email):
    """Count user's chats"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM chats WHERE user_email = ?', (user_email,))
        return cursor.fetchone()[0]
    finally:
        conn.close()


# Auto-initialize
init_chat_db()


# ========================================
# TESTING
# ========================================
if __name__ == "__main__":
    print("Testing Chat History Database...")
    
    # Create a chat
    cid = create_chat("test@user.com", "Test Chat")
    print(f"Created chat: {cid}")
    
    # Add messages
    add_message(cid, "user", "Hello!")
    add_message(cid, "assistant", "Hi there!")
    
    # Get messages
    msgs = get_chat_messages(cid)
    print(f"Messages: {len(msgs)}")
    
    # Get user chats
    chats = get_user_chats("test@user.com")
    print(f"User chats: {len(chats)}")
    
    # Cleanup
    delete_chat(cid)
    print("✅ All tests passed!")