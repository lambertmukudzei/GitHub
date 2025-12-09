from app.data.db import connect_database

def create_users_table(conn):
    """Create users table for authentication"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ Users table created successfully!")

def create_cyber_incidents_table(conn):
    """Create cyber_incidents table - MATCHES YOUR CSV STRUCTURE"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id INTEGER PRIMARY KEY,
            timestamp TEXT,
            severity TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ Cyber incidents table created successfully!")

def create_datasets_metadata_table(conn):
    """Create datasets_metadata table - MATCHES YOUR CSV STRUCTURE"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            dataset_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            rows INTEGER,
            columns INTEGER,
            uploaded_by TEXT,
            upload_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ Datasets metadata table created successfully!")

def create_it_tickets_table(conn):
    """Create it_tickets table - MATCHES YOUR CSV STRUCTURE"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            ticket_id INTEGER PRIMARY KEY,
            priority TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            assigned_to TEXT,
            created_at TEXT,
            resolution_time_hours INTEGER,
            created_at_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ IT tickets table created successfully!")

def create_all_tables(conn):
    """Create all database tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("🎉 All tables created successfully!")