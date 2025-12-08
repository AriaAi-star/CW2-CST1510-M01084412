import pandas as pd
import sqlite3



def migrate_metadata(conn):
    """we wanna change  the databese meteadata from csv to sql"""
    data_metadata=pd.read_csv('DATA/datasets_metadata.csv')
    data_metadata.to_sql('datasets_metadata',conn,if_exists='replace',index=False)



def get_all_datasets_metadata(conn):
    """Retrieve all datasets metadata from database."""
    query="SELECT * FROM datasets_metadata"
    return pd.read_sql_query(query,conn)

