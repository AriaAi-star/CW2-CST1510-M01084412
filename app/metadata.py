import pandas as pd
import sqlite3

def migrate_metadata(conn):
    data_metadata = pd.read_csv('DATA/datasets_metadata.csv')
    data_metadata.to_sql('datasets_metadata', conn, if_exists='replace', index=False)


