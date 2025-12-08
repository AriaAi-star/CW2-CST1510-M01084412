import pandas as pd
from app.db import connect_database

def insert_incident(timestamp, severity, category, status, description):
    """Insert new incident into database."""
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


def delete_incident(conn, incident_id):
    """Delete an incident from the database."""
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE incident_id = ?",
        (incident_id,)
    )
    conn.commit()
    return cursor.rowcount
