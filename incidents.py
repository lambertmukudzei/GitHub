import pandas as pd
import sqlite3
from app.data.db import connect_database

def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """Insert a new cyber incident - UPDATED FOR NEW SCHEMA"""
    conn = connect_database()
    cursor = conn.cursor()
    
    try:
        # For the new schema, we're using auto-increment ID, so we don't specify incident_id
        cursor.execute("""
            INSERT INTO cyber_incidents 
            (timestamp, severity, category, status, description)
            VALUES (?, ?, ?, ?, ?)
        """, (date, severity, incident_type, status, description))
        
        conn.commit()
        incident_id = cursor.lastrowid
        conn.close()
        return incident_id
    except sqlite3.Error as e:
        conn.close()
        print(f"❌ Error inserting incident: {e}")
        return None

def get_all_incidents():
    """Retrieve all incidents."""
    conn = connect_database()
    try:
        df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY incident_id DESC", conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        print(f"❌ Error reading incidents: {e}")
        return pd.DataFrame()

def update_incident_status(incident_id, new_status):
    """Update incident status."""
    conn = connect_database()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?",
            (new_status, incident_id)
        )
        conn.commit()
        rows_updated = cursor.rowcount
        conn.close()
        return rows_updated
    except sqlite3.Error as e:
        conn.close()
        print(f"❌ Error updating incident: {e}")
        return 0

def delete_incident(incident_id):
    """Delete an incident."""
    conn = connect_database()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM cyber_incidents WHERE incident_id = ?", (incident_id,))
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()
        return rows_deleted
    except sqlite3.Error as e:
        conn.close()
        print(f"❌ Error deleting incident: {e}")
        return 0
