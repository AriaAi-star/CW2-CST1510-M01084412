
import sqlite3
import pandas as pd
#


df = pd.DataFrame(
    {

        'year': [2020, 2021, 2022],
        'value': [100, 200, 300]
    }
)




#conn = sqlite3.connect('DATA/cyber_incidents.db')  
# 
def migrate_data(conn):
    data_cyber = pd.read_csv('DATA/cyber_incidents.csv')
    data_cyber.to_sql('cyber_incidents', conn, if_exists='replace', index=False)    




def migrate_metadata(conn):
    data_metadata = pd.read_csv('DATA/datasets_metadata.csv')
    data_metadata.to_sql('datasets_metadata', conn, if_exists='replace', index=False)


def migrate_datasets_metadata(conn):
    data_datasets = pd.read_csv('DATA/datasets.csv')
    data_datasets.to_sql('datasets', conn, if_exists='replace', index=False)



conn = sqlite3.connect('DATA/inteligent_platform.db')
sql = 'SELECT * FROM cyber_incidents'
data = pd.read_sql(sql, conn)
conn.close()

print(data.head())