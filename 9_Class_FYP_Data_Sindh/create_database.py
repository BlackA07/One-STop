# Script 1: create_database.py
import sqlite3

DATABASE_FILE = 'knowledge.db'
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# Create a new table for the knowledge base
cursor.execute('''
    CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY,
        category TEXT,
        subject TEXT,
        source_file TEXT,
        text_chunk TEXT
    )
''')
conn.commit()
conn.close()
print(f"Success! Database '{DATABASE_FILE}' has been created and the table is ready.")