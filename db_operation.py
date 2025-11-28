"""Database migration operations.

This module provides functions to migrate data from CSV files into the SQLite database.
"""

import sqlite3
import pandas as pd
from app.db import connect_database


def migrate_cyber_incidents(conn):
    """Migrate cyber incidents from CSV to database."""
    data_cyber = pd.read_csv('DATA/cyber_incidents.csv')
    data_cyber.to_sql('cyber_incidents', conn, if_exists='replace', index=False)
    print(f"✅ Migrated {len(data_cyber)} cyber incidents")


def migrate_datasets_metadata(conn):
    """Migrate dataset metadata from CSV to database."""
    data_metadata = pd.read_csv('DATA/datasets_metadata.csv')
    data_metadata.to_sql('datasets_metadata', conn, if_exists='replace', index=False)
    print(f"✅ Migrated {len(data_metadata)} metadata records")


if __name__ == "__main__":
    """Run migrations when executed directly."""
    conn = connect_database()
    
    try:
        migrate_cyber_incidents(conn)
        migrate_datasets_metadata(conn)
        print("\n✅ All migrations completed successfully!")
    except Exception as e:
        print(f"❌ Migration error: {e}")
    finally:
        conn.close()
