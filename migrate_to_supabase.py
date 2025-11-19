import sqlite3
from supabase import create_client, Client

# --- Configuration ---
# 1. Paste your local DB name
LOCAL_DB_FILE = 'knowledge.db'

# 2. Paste your Supabase project URL and Key
SUPABASE_URL = "https://ifbknohkqfqplwvocksc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlmYmtub2hrcWZxcGx3dm9ja3NjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg4NjIyMjIsImV4cCI6MjA3NDQzODIyMn0.a5motl3g-arn6B-_JmL4J6WhmwacAkesfW1LnD52FQY"

# --- Script ---
def migrate_data():
    print("Connecting to local SQLite database...")
    # Connect to local SQLite DB
    conn = sqlite3.connect(LOCAL_DB_FILE)
    conn.row_factory = sqlite3.Row # This lets us read data as a dictionary
    cursor = conn.cursor()

    print("Connecting to Supabase...")
    # Connect to Supabase
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    print("Reading data from local 'knowledge' table...")
    cursor.execute("SELECT category, subject, source_file, text_chunk FROM knowledge")
    rows = cursor.fetchall()

    if not rows:
        print("No data found in local database.")
        return

    print(f"Found {len(rows)} rows to migrate. Preparing data...")

    # Convert SQLite rows to a list of dictionaries for Supabase
    data_to_insert = []
    for row in rows:
        data_to_insert.append(dict(row))

    print("Uploading data to Supabase 'knowledge' table...")
    # Insert data in batches (Supabase can handle many at once)
    data, count = supabase.table('knowledge').insert(data_to_insert).execute()

    print(f"--- Migration Complete! ---")
    print(f"Successfully inserted {len(data[1])} rows into Supabase.")

if __name__ == "__main__":
    migrate_data()