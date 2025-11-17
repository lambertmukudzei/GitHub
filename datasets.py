import pandas as pd
from app.data.db import connect_database

def get_all_datasets():
    """I must now Get all datasets."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
    conn.close()
    return df