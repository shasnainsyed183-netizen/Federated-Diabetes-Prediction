"""
MediFederate Prediction History Database
SQLite-based storage for all AI predictions
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os


DB_PATH = 'predictions_history.db'


def init_database():
    """Create database and tables if not exists"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            disease TEXT NOT NULL,
            probability REAL NOT NULL,
            risk_level TEXT NOT NULL,
            patient_data TEXT NOT NULL,
            notes TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def save_prediction(disease, probability, risk_level, patient_data, notes=""):
    """Save a single prediction to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO predictions (timestamp, disease, probability, risk_level, patient_data, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        disease,
        float(probability),
        risk_level,
        str(patient_data),
        notes
    ))
    
    conn.commit()
    prediction_id = cursor.lastrowid
    conn.close()
    
    return prediction_id


def get_all_predictions(disease_filter=None, limit=500):
    """Get all predictions from database"""
    conn = sqlite3.connect(DB_PATH)
    
    if disease_filter and disease_filter != "All":
        query = "SELECT * FROM predictions WHERE disease = ? ORDER BY id DESC LIMIT ?"
        df = pd.read_sql_query(query, conn, params=(disease_filter, limit))
    else:
        query = "SELECT * FROM predictions ORDER BY id DESC LIMIT ?"
        df = pd.read_sql_query(query, conn, params=(limit,))
    
    conn.close()
    return df


def get_statistics():
    """Get statistics for dashboard"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    stats = {}
    
    cursor.execute("SELECT COUNT(*) FROM predictions")
    stats['total'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE risk_level = 'High Risk'")
    stats['high_risk'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE risk_level = 'Low Risk'")
    stats['low_risk'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE disease = 'Diabetes'")
    stats['diabetes'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE disease = 'Heart Disease'")
    stats['heart'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE disease = 'Stroke'")
    stats['stroke'] = cursor.fetchone()[0]
    
    conn.close()
    return stats


def delete_prediction(prediction_id):
    """Delete a single prediction"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE id = ?", (prediction_id,))
    conn.commit()
    conn.close()


def clear_all_predictions():
    """Delete all predictions"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()


def export_to_csv():
    """Export all predictions to CSV"""
    df = get_all_predictions(limit=10000)
    return df.to_csv(index=False).encode('utf-8')


def get_disease_distribution():
    """Get count of predictions per disease"""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT disease, COUNT(*) as count FROM predictions GROUP BY disease"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_risk_distribution():
    """Get count of high vs low risk"""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT risk_level, COUNT(*) as count FROM predictions GROUP BY risk_level"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# Auto-initialize on import
init_database()


# ========================================
# TESTING
# ========================================
if __name__ == "__main__":
    print("Testing History Database...")
    
    # Save test predictions
    save_prediction(
        "Diabetes", 0.42, "Low Risk",
        {"age": 55, "meds": 15, "time": 5}
    )
    save_prediction(
        "Heart Disease", 0.81, "High Risk",
        {"age": 65, "bp": 150, "chol": 280}
    )
    save_prediction(
        "Stroke", 0.26, "Low Risk",
        {"age": 45, "bmi": 24, "glucose": 95}
    )
    
    print("\n✅ Test data saved!")
    
    # Get stats
    stats = get_statistics()
    print(f"\nStatistics:")
    print(f"  Total predictions: {stats['total']}")
    print(f"  High risk: {stats['high_risk']}")
    print(f"  Low risk: {stats['low_risk']}")
    print(f"  Diabetes: {stats['diabetes']}")
    print(f"  Heart: {stats['heart']}")
    print(f"  Stroke: {stats['stroke']}")
    
    # Get all
    df = get_all_predictions()
    print(f"\nFirst few rows:")
    print(df.head())