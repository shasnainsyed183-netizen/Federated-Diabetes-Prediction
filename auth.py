"""
MediFederate Authentication Module
User registration, login, and password reset with bcrypt
"""

import sqlite3
import bcrypt
import re
from datetime import datetime


AUTH_DB_PATH = 'users.db'


def _get_connection():
    """Get a fresh database connection with timeout"""
    conn = sqlite3.connect(AUTH_DB_PATH, timeout=15)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_auth_database():
    """Create users table if not exists"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL,
                role TEXT DEFAULT 'doctor',
                hospital TEXT,
                created_at TEXT NOT NULL,
                last_login TEXT
            )
        ''')
        conn.commit()
    finally:
        conn.close()


def _is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def _is_valid_password(password):
    return len(password) >= 6


def signup(full_name, email, password, hospital="", role="doctor"):
    """Register a new user"""
    if not full_name or len(full_name.strip()) < 2:
        return False, "Full name must be at least 2 characters.", None
    if not _is_valid_email(email):
        return False, "Please enter a valid email address.", None
    if not _is_valid_password(password):
        return False, "Password must be at least 6 characters long.", None
    
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password_bytes, salt)
    
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (full_name, email, password_hash, role, hospital, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            full_name.strip(),
            email.lower().strip(),
            password_hash,
            role,
            hospital.strip(),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        user_id = cursor.lastrowid
        
        user_data = {
            'id': user_id,
            'full_name': full_name.strip(),
            'email': email.lower().strip(),
            'role': role,
            'hospital': hospital.strip()
        }
        return True, "Account created successfully!", user_data
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists.", None
    except Exception as e:
        return False, f"Error creating account: {str(e)}", None
    finally:
        if conn:
            conn.close()


def login(email, password):
    """Login a user"""
    if not email or not password:
        return False, "Please enter both email and password.", None
    
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, full_name, email, password_hash, role, hospital
            FROM users WHERE email = ?
        ''', (email.lower().strip(),))
        
        row = cursor.fetchone()
        
        if not row:
            return False, "Invalid email or password.", None
        
        user_id, full_name, db_email, password_hash, role, hospital = row
        
        if bcrypt.checkpw(password.encode('utf-8'), password_hash):
            cursor.execute('''
                UPDATE users SET last_login = ? WHERE id = ?
            ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
            conn.commit()
            
            user_data = {
                'id': user_id,
                'full_name': full_name,
                'email': db_email,
                'role': role,
                'hospital': hospital
            }
            return True, "Login successful!", user_data
        else:
            return False, "Invalid email or password.", None
    except Exception as e:
        return False, f"Login error: {str(e)}", None
    finally:
        if conn:
            conn.close()


def reset_password(email, new_password):
    """
    Reset a user's password (for forgot password flow)
    Returns: (success: bool, message: str)
    """
    if not email or not new_password:
        return False, "Please provide both email and new password."
    
    if not _is_valid_email(email):
        return False, "Please enter a valid email address."
    
    if not _is_valid_password(new_password):
        return False, "Password must be at least 6 characters long."
    
    # Check if user exists
    if not email_exists(email):
        return False, "No account found with this email address."
    
    # Hash new password
    password_bytes = new_password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password_bytes, salt)
    
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET password_hash = ? WHERE email = ?
        ''', (password_hash, email.lower().strip()))
        conn.commit()
        
        if cursor.rowcount > 0:
            return True, "Password reset successfully! Please login with your new password."
        else:
            return False, "Failed to reset password. Please try again."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        if conn:
            conn.close()


def get_user_count():
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]
    finally:
        conn.close()


def email_exists(email):
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email.lower().strip(),))
        return cursor.fetchone() is not None
    finally:
        conn.close()


def get_all_users():
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, full_name, email, role, hospital, created_at, last_login
            FROM users ORDER BY id DESC
        ''')
        return cursor.fetchall()
    finally:
        conn.close()


def delete_user(user_id):
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
    finally:
        conn.close()


# Auto-initialize
init_auth_database()


# ========================================
# TESTING
# ========================================
if __name__ == "__main__":
    print("Testing Authentication Module...\n")
    
    # Test signup
    success, msg, user = signup("Dr. Test User", "test@medifederate.pk", "secure123", "Test Hospital")
    print(f"Signup: {success} - {msg}")
    
    # Test duplicate
    success, msg, _ = signup("Dr. Test", "test@medifederate.pk", "secure123", "Test Hospital")
    print(f"Duplicate signup: {success} - {msg}")
    
    # Test login
    success, msg, user = login("test@medifederate.pk", "secure123")
    print(f"Login: {success} - {msg}")
    
    # Test reset password
    success, msg = reset_password("test@medifederate.pk", "newpass123")
    print(f"Reset password: {success} - {msg}")
    
    # Test login with new password
    success, msg, user = login("test@medifederate.pk", "newpass123")
    print(f"Login with new password: {success} - {msg}")
    
    # Test reset for non-existent email
    success, msg = reset_password("nonexistent@test.com", "newpass")
    print(f"Reset non-existent: {success} - {msg}")