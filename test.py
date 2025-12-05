# Simple test file

from app.db import connect_database

conn = connect_database()
print("Database connected!")
conn.close()





