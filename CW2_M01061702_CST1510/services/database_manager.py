# My database_manager.py
# Student iD: M01061702
# This file handles all database operations, like a librarian for data
import sqlite3
from typing import Any, Iterable, List, Tuple
from pathlib import Path

class DatabaseManager:
    """Handles SQLite database connections and queries (thread-safe)."""
    
    def __init__(self, db_path: str = "DATA/intelligence_platform.db"):
        # Set the database file location
        self._db_path = db_path
        
        # Check if database file exists
        if not Path(self._db_path).exists():
            print(f"⚠️ Database not found at: {self._db_path}")
            print("   Make sure your CSV files are imported into the database.")
    
    def _get_connection(self) -> sqlite3.Connection:
        """Create a new connection to the database."""
        # Connect to the SQLite database file
        return sqlite3.connect(self._db_path, check_same_thread=False)
    
    def execute_query(self, sql: str, params: Iterable[Any] = ()) -> sqlite3.Cursor:
        """Execute a write query (INSERT, UPDATE, DELETE)."""
        # Open connection, run command, save changes, close connection
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, tuple(params))  # Run the SQL command
            conn.commit()  # Save changes to database
            return cur  # Return cursor (contains results)
    
    def fetch_one(self, sql: str, params: Iterable[Any] = ()) -> Tuple | None:
        """Fetch a single row from the database."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, tuple(params))
            return cur.fetchone()  # Get first row or None
    
    def fetch_all(self, sql: str, params: Iterable[Any] = ()) -> List[Tuple]:
        """Fetch all rows from the database."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, tuple(params))
            return cur.fetchall()  # Get all rows as list
    
    def get_table_structure(self, table_name: str) -> List[Tuple]:
        """Get column information for a table."""
        # PRAGMA table_info shows columns, types, etc.
        return self.fetch_all(f"PRAGMA table_info({table_name})")
    
    def get_all_tables(self) -> List[str]:
        """Get list of all tables in the database."""
        rows = self.fetch_all("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in rows]  # Extract table names
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        result = self.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return result is not None  # True if table exists