import pandas as pd
from app.data.db import connect_database

def get_all_tickets():
    """I must Get all tickets."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)
    conn.close()
    return df