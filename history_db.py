"""
MediFederate Prediction History Database
SQLite-based storage with per-user filtering
"""

import sqlite3
import pandas as pd
from datetime import datetime


DB_PATH = 'predictions_history.db'


def _get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_database():
    """Create database and tables if not exists (with migration)"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_email TEXT,
                disease TEXT NOT NULL,
                probability REAL NOT NULL,
                risk_level TEXT NOT NULL,
                patient_data TEXT NOT NULL,
                notes TEXT
            )
        ''')
        
        cursor.execute("PRAGMA table_info(predictions)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'user_email' not in columns:
            cursor.execute("ALTER TABLE predictions ADD COLUMN user_email TEXT")
        
        conn.commit()
    finally:
        conn.close()


def save_prediction(disease, probability, risk_level, patient_data, notes="", user_email=None):
    """Save a single prediction to database"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (timestamp, user_email, disease, probability, risk_level, patient_data, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            user_email or 'guest@medifederate',
            disease,
            float(probability),
            risk_level,
            str(patient_data),
            notes
        ))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_all_predictions(disease_filter=None, limit=500, user_email=None):
    """
    Get predictions — optionally filtered by user_email
    If user_email is None → returns all (admin mode)
    """
    conn = _get_connection()
    try:
        params = []
        query = "SELECT * FROM predictions"
        conditions = []
        
        if user_email:
            conditions.append("user_email = ?")
            params.append(user_email)
        
        if disease_filter and disease_filter != "All":
            conditions.append("disease = ?")
            params.append(disease_filter)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        
        df = pd.read_sql_query(query, conn, params=tuple(params))
        return df
    finally:
        conn.close()


def get_user_predictions(user_email, limit=10):
    """Get predictions for a specific user"""
    if not user_email:
        return pd.DataFrame()
    
    conn = _get_connection()
    try:
        query = "SELECT * FROM predictions WHERE user_email = ? ORDER BY id DESC LIMIT ?"
        return pd.read_sql_query(query, conn, params=(user_email, limit))
    finally:
        conn.close()


def get_statistics(user_email=None):
    """Get statistics — optionally user-specific"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        stats = {}
        
        where = "WHERE user_email = ?" if user_email else ""
        params = (user_email,) if user_email else ()
        
        cursor.execute(f"SELECT COUNT(*) FROM predictions {where}", params)
        stats['total'] = cursor.fetchone()[0]
        
        cursor.execute(
            f"SELECT COUNT(*) FROM predictions {where} {'AND' if where else 'WHERE'} risk_level = 'High Risk'",
            params
        )
        stats['high_risk'] = cursor.fetchone()[0]
        
        cursor.execute(
            f"SELECT COUNT(*) FROM predictions {where} {'AND' if where else 'WHERE'} risk_level = 'Low Risk'",
            params
        )
        stats['low_risk'] = cursor.fetchone()[0]
        
        for disease in ['Diabetes', 'Heart Disease', 'Stroke', 'Kidney Disease']:
            cursor.execute(
                f"SELECT COUNT(*) FROM predictions {where} {'AND' if where else 'WHERE'} disease = ?",
                params + (disease,)
            )
            stats[disease.lower().replace(' ', '_')] = cursor.fetchone()[0]
        
        return stats
    finally:
        conn.close()


def delete_prediction(prediction_id):
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions WHERE id = ?", (prediction_id,))
        conn.commit()
    finally:
        conn.close()


def clear_all_predictions(user_email=None):
    """Clear all predictions — optionally user-specific"""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        if user_email:
            cursor.execute("DELETE FROM predictions WHERE user_email = ?", (user_email,))
        else:
            cursor.execute("DELETE FROM predictions")
        conn.commit()
    finally:
        conn.close()


def export_to_csv(user_email=None):
    """Export predictions to CSV — optionally user-specific"""
    df = get_all_predictions(user_email=user_email, limit=10000)
    return df.to_csv(index=False).encode('utf-8')


def get_disease_distribution(user_email=None):
    """Get count per disease — optionally user-specific"""
    conn = _get_connection()
    try:
        if user_email:
            query = "SELECT disease, COUNT(*) as count FROM predictions WHERE user_email = ? GROUP BY disease"
            return pd.read_sql_query(query, conn, params=(user_email,))
        else:
            query = "SELECT disease, COUNT(*) as count FROM predictions GROUP BY disease"
            return pd.read_sql_query(query, conn)
    finally:
        conn.close()


def get_risk_distribution(user_email=None):
    """Get risk distribution — optionally user-specific"""
    conn = _get_connection()
    try:
        if user_email:
            query = "SELECT risk_level, COUNT(*) as count FROM predictions WHERE user_email = ? GROUP BY risk_level"
            return pd.read_sql_query(query, conn, params=(user_email,))
        else:
            query = "SELECT risk_level, COUNT(*) as count FROM predictions GROUP BY risk_level"
            return pd.read_sql_query(query, conn)
    finally:
        conn.close()


# Auto-initialize
init_database()


# ========================================
# TESTING
# ========================================
if __name__ == "__main__":
    print("Testing History Database...")
    
    save_prediction("Diabetes", 0.42, "Low Risk", {"age": 55}, user_email="doc1@test.com")
    save_prediction("Heart Disease", 0.81, "High Risk", {"age": 65}, user_email="doc1@test.com")
    save_prediction("Kidney Disease", 0.30, "Low Risk", {"age": 45}, user_email="doc2@test.com")
    
    print(f"\nDoc1 predictions: {len(get_user_predictions('doc1@test.com'))}")
    print(f"Doc2 predictions: {len(get_user_predictions('doc2@test.com'))}")
    print(f"All predictions: {len(get_all_predictions(user_email=None))}")
    
    stats_doc1 = get_statistics(user_email="doc1@test.com")
    print(f"\nDoc1 stats: Total={stats_doc1['total']}, High={stats_doc1['high_risk']}")
    
    stats_all = get_statistics()
    print(f"Global stats: Total={stats_all['total']}")