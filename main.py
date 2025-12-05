# Simple database test

from app.db import connect_database
from app.incidents import get_all_incidents

# Connect
conn = connect_database()
print("Connected!")

# Get data
incidents = get_all_incidents()
print(f"\nTotal incidents: {len(incidents)}")
print(incidents.head(3))

conn.close()

