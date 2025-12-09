import pandas as pd
from app.data.db import connect_database

def get_all_tickets():
    """Get all IT tickets."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df