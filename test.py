import pandas as pd
from app.metadata import get_all_datasets_metadata
import sqlite3

from db_operation import connect_database
#

conn = connect_database()
data = get_all_datasets_metadata(conn)
conn.close()

print(data)





