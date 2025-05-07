import os
import csv
import sqlite3

# 1. Paths – adjust if needed.
BASE_DIR = os.getcwd()
CSV_PATH = os.path.join(BASE_DIR, "../output/File.csv")
DB_PATH  = os.path.join(BASE_DIR, "test3.db")

# 2. Connect to your existing SQLite database.
conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

# 3. Prepare the INSERT statement (match your table’s columns exactly).
insert_sql = """
    INSERT INTO Word (Word, Filename, Count)
    VALUES (?, ?, ?)
"""

# 4. Read CSV and batch‑insert.
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=",")
    batch  = []
    for row in reader:
        # Convert Count to int (or remove if your schema auto‑casts)
        batch.append((
            row["word"],
            row["Filename"],
            int(row["Count"])
        ))

# 5. Execute in a single batch for speed.
cur.executemany(insert_sql, batch)
conn.commit()

print(f"Appended {len(batch)} rows into 'word_counts' in {DB_PATH}")

# 6. Close up.
cur.close()
conn.close()