# INSTRUCTOR
'''
# import sqlite3

# Connect to the database (or create it if it doesn’t exist)
conn = sqlite3.connect('example.db')

# Create a cursor object
cur = conn.cursor()

# Create a table

cur.execute (
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
            )

# Insert one row
cur.execute(
    "INSERT INTO users (name, age) VALUES (?, ?)",
    ('Alice', 30)
)

# Save (commit) the change

'''
