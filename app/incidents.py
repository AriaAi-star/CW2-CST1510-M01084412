import pandas as pd
from app.db import connect_database

def insert_incident(timestamp,severity,category,status,description):
    """
         Add new incident. Matches the columns in `DATA/cyber_inc
         Note: the csv file headers are "incident_id, timestamp, severity, category, 
         status, description <code>incident_id</code> isn’t auto-populated in the
         table; the value must be passed in.
    
    """
    conn=connect_database()
    cursor=conn.cursor()
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
    """
    Delete an incident from the database.
    Args:
        conn: SQLite database connection
        incident_id: ID of the incident to delete
    Returns:
        Number of rows deleted (0 or 1)
    """
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE incident_id = ?",
        (incident_id,)
    )
    conn.commit()
    return cursor.rowcount
