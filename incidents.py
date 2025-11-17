import pandas as pd
from pathlib import Path
from app.data.db import connect_database

def load_csv_to_table(conn, csv_path, table_name):
    #Firstly we Load CSV data into database table.
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return 0
    
    try:
        df = pd.read_csv(csv_path)
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        row_count = len(df)
        print(f"Loaded {row_count} rows from {csv_path.name} into {table_name}")
        return row_count
    except Exception as e:
        print(f"Error loading {csv_path.name}: {e}")
        return 0

def load_all_csv_data(conn):
    #Here we Load all CSV files into database.
    csv_mappings = [
        (Path("DATA") / "cyber_incidents.csv", "cyber_incidents"),
        (Path("DATA") / "datasets_metadata.csv", "datasets_metadata"), 
        (Path("DATA") / "it_tickets.csv", "it_tickets")
    ]
    
    total_rows = 0
    for csv_path, table_name in csv_mappings:
        rows_loaded = load_csv_to_table(conn, csv_path, table_name)
        total_rows += rows_loaded
    
    return total_rows

def insert_incident(timestamp, severity, category, status, description):
    #Insert new cyber incident.
    conn = connect_database()
    cursor = conn.cursor()
    
    # Now here i should Get the next incident_id (max + 1)
    cursor.execute("SELECT MAX(incident_id) FROM cyber_incidents")
    max_id = cursor.fetchone()[0] or 0
    next_id = max_id + 1
    
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (incident_id, timestamp, severity, category, status, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (next_id, timestamp, severity, category, status, description))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    #Here we Get all incidents.
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY incident_id DESC", conn)
    conn.close()
    return df

def update_incident_status(incident_id, new_status):
    #We must Update incident status.
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE incident_id = ?", (new_status, incident_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected

def delete_incident(incident_id):
    #I must now Delete incident.
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE incident_id = ?", (incident_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected