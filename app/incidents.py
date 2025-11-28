import pandas as pd
from app.db import connect_database

def insert_incident(timestamp, severity, category, status, description):
    """Insert new incident. Matches columns in `DATA/cyber_incidents.csv`.

    Note: the CSV uses `incident_id, timestamp, severity, category, status, description`.
    `incident_id` is not auto-generated here; callers should supply or DB will assign rowid.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO cyber_incidents
        (timestamp, severity, category, status, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        (timestamp, severity, category, status, description),
    )
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY incident_id DESC",
        conn,
    )
    conn.close()
    return df