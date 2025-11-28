"""Main entry point for the Cyber Incidents application.

Demonstrates basic database connectivity and CRUD operations.
"""

from app.db import connect_database
from app.incidents import insert_incident, get_all_incidents
from app.metadata import get_all_datasets_metadata


def main():
    """Demonstrate database operations."""
    print("=" * 60)
    print("Cyber Incidents Platform - Demo")
    print("=" * 60)
    
    # 1. Setup database connection
    conn = connect_database()
    print("✓ Connected to database")
    
    # 2. Test metadata retrieval
    try:
        metadata_df = get_all_datasets_metadata(conn)
        print(f"✓ Loaded {len(metadata_df)} datasets from metadata")
    except Exception as e:
        print(f"✗ Error loading metadata: {e}")
    
    # 3. Test incident retrieval
    try:
        incidents_df = get_all_incidents()
        print(f"✓ Found {len(incidents_df)} incidents in database")
        if len(incidents_df) > 0:
            print(f"  Sample incident:\n{incidents_df.iloc[0]}")
    except Exception as e:
        print(f"✗ Error loading incidents: {e}")
    
    # 4. Test inserting new incident
    try:
        incident_id = insert_incident(
            timestamp="2024-11-28",
            severity="Medium",
            category="Malware",
            status="Open",
            description="Test incident from main.py"
        )
        print(f"✓ Created incident #{incident_id}")
    except Exception as e:
        print(f"✗ Error creating incident: {e}")
    
    conn.close()
    print("=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

