import sqlite3
from pathlib import Path

db_path = Path("DATA") / "intelligence_platform.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("UPDATE users SET role = 'Security Analyst' WHERE username LIKE '%sec%' OR username LIKE '%cyber%'")
cursor.execute("UPDATE users SET role = 'Data Scientist' WHERE username LIKE '%data%' OR username LIKE '%analyst%'")
cursor.execute("UPDATE users SET role = 'IT Support' WHERE username LIKE '%it%' OR username LIKE '%support%' OR username LIKE '%admin%'")
cursor.execute("UPDATE users SET role = 'General User' WHERE role = 'user'")

conn.commit()
conn.close()
print("User roles updated successfully!")
    """)