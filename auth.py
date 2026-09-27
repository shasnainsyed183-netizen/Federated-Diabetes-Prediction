"""
MediFederate Authentication Module
User registration, login, and session management with bcrypt password hashing
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
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def _is_valid_password(password):
    """Password must be at least 6 characters"""
    return len(password) >= 6


def signup(full_name, email, password, hospital="", role="doctor"):
    """
    Register a new user
    Returns: (success: bool, message: str, user_data: dict or None)
    """
    # Validations
    if not full_name or len(full_name.strip()) < 2:
        return False, "Full name must be at least 2 characters.", None

    if not _is_valid_email(email):
        return False, "Please enter a valid email address.", None

    if not _is_valid_password(password):
        return False, "Password must be at least 6 characters long.", None

    # Hash password with bcrypt
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
    """
    Login a user
    Returns: (success: bool, message: str, user_data: dict or None)
    """
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

        # Verify password
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


def get_user_count():
    """Get total number of registered users"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        return count
    finally:
        conn.close()


def email_exists(email):
    """Check if email is already registered"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email.lower().strip(),))
        result = cursor.fetchone()
        return result is not None
    finally:
        conn.close()


def get_all_users():
    """Get all users (for admin)"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, full_name, email, role, hospital, created_at, last_login
            FROM users ORDER BY id DESC
        ''')
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()


def delete_user(user_id):
    """Delete a user by ID"""
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

    success, msg, user = signup(
        "Dr. Ahmed Khan",
        "ahmed@medifederate.pk",
        "secure123",
        "Aga Khan Hospital"
    )
    print(f"Signup: {success} - {msg}")
    if user:
        print(f"  User: {user}")

    success, msg, _ = signup(
        "Dr. Ahmed Khan",
        "ahmed@medifederate.pk",
        "secure123",
        "Aga Khan Hospital"
    )
    print(f"Duplicate signup: {success} - {msg}")

    success, msg, user = login("ahmed@medifederate.pk", "secure123")
    print(f"Correct login: {success} - {msg}")

    success, msg, user = login("ahmed@medifederate.pk", "wrongpass")
    print(f"Wrong password: {success} - {msg}")

    success, msg, _ = signup("Test", "invalid-email", "pass123")
    print(f"Invalid email: {success} - {msg}")

    success, msg, _ = signup("Test User", "test@test.com", "123")
    print(f"Short password: {success} - {msg}")

    print(f"\nTotal users: {get_user_count()}")