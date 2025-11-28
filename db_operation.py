"""Database migration operations.

This module provides functions to migrate data from CSV files into the SQLite database.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional
from app.db import connect_database


try:
    from sqlalchemy import create_engine
    _HAS_SQLALCHEMY = True
except Exception:
    _HAS_SQLALCHEMY = False


def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.
    
    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table
        
    Returns:
        int: Number of rows loaded
    """
    # Default simple wrapper kept for backward compatibility
    return _load_csv_to_table(
        conn,
        csv_path,
        table_name,
    )


def _load_csv_to_table(
    conn,
    csv_path: str,
    table_name: str,
    if_exists: str = 'append',
    chunksize: Optional[int] = None,
    use_sqlalchemy: bool = False,
    dtype: Optional[dict] = None,
    progress: bool = False,
):
    """Robust CSV -> SQL loader.

    Features:
    - checks file existence
    - optional chunked loading to avoid OOM
    - transaction support (commit/rollback)
    - optional SQLAlchemy engine for faster multi-row inserts

    Returns number of rows inserted.
    """
    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"⚠️ File not found: {csv_path}")
        return 0

    total_inserted = 0
    first_chunk = True

    # Prepare SQLAlchemy engine if requested and available
    engine = None
    if use_sqlalchemy:
        if not _HAS_SQLALCHEMY:
            print("⚠️ SQLAlchemy not available; falling back to sqlite3 connection")
            use_sqlalchemy = False
        else:
            # Build a file-based sqlite URL from the sqlite3 connection
            try:
                # Attempt to infer DB file path from connection
                db_path = conn.execute("PRAGMA database_list;").fetchall()[0][2]
                engine = create_engine(f"sqlite:///{db_path}")
            except Exception:
                use_sqlalchemy = False

    # Begin a transaction scope using the sqlite3 connection
    try:
        conn.execute('BEGIN')

        if chunksize and chunksize > 0:
            for chunk in pd.read_csv(csv_path, chunksize=chunksize, dtype=dtype):
                if use_sqlalchemy and engine is not None:
                    # For first chunk, respect if_exists, subsequent chunks must append
                    chunk.to_sql(
                        table_name,
                        engine,
                        if_exists=(if_exists if first_chunk else 'append'),
                        index=False,
                        method='multi',
                    )
                else:
                    chunk.to_sql(
                        table_name,
                        conn,
                        if_exists=(if_exists if first_chunk else 'append'),
                        index=False,
                    )

                rows = len(chunk)
                total_inserted += rows
                first_chunk = False
                if progress:
                    print(f"Loaded chunk: {rows} rows (total: {total_inserted})")
        else:
            df = pd.read_csv(csv_path, dtype=dtype)
            if use_sqlalchemy and engine is not None:
                df.to_sql(table_name, engine, if_exists=if_exists, index=False, method='multi')
            else:
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            total_inserted = len(df)

        conn.commit()
        print(f"✅ Loaded {total_inserted} rows into {table_name}")
        return total_inserted

    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print(f"❌ Failed to load CSV into {table_name}: {e}")
        raise


def load_all_csv_data(
    conn,
    mapping: Optional[dict] = None,
    if_exists: str = 'replace',
    chunksize: Optional[int] = None,
    use_sqlalchemy: bool = False,
    progress: bool = False,
):
    """Load multiple CSV files into their target tables in sequence.

    Args:
        conn: sqlite3.Connection
        mapping: dict mapping table_name -> csv_path. If None, uses project defaults.
        if_exists: behavior for to_sql ('replace'|'append'|'fail')
        chunksize: optional chunk size for streaming
        use_sqlalchemy: whether to try using SQLAlchemy engine
        progress: print per-file progress

    Returns:
        dict: table_name -> rows_inserted or error string
    """
    # default mapping for this project
    default_mapping = {
        'cyber_incidents': 'DATA/cyber_incidents.csv',
        'datasets_metadata': 'DATA/datasets_metadata.csv',
    }

    if mapping is None:
        mapping = default_mapping

    results = {}
    for table_name, csv_path in mapping.items():
        if progress:
            print(f"[load_all_csv_data] Loading {csv_path} -> {table_name}")
        try:
            inserted = _load_csv_to_table(
                conn,
                csv_path,
                table_name,
                if_exists=if_exists,
                chunksize=chunksize,
                use_sqlalchemy=use_sqlalchemy,
                progress=progress,
            )
            results[table_name] = inserted
        except Exception as e:
            results[table_name] = f"error: {e}"
    return results


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
