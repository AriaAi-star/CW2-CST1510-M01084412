import pandas as pd
from app.metadata import get_all_datasets_metadata
from app.db import connect_database

conn = connect_database()
data = get_all_datasets_metadata(conn)
conn.close()

print(data)





