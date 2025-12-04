"""IT Tickets management module."""


def create_it_tickets_table(conn):
    """Create the it_tickets table if it doesn't exist.
    
    Required columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - ticket_id: TEXT UNIQUE NOT NULL
    - priority: TEXT (e.g., 'Critical', 'High', 'Medium', 'Low')
    - status: TEXT (e.g., 'Open', 'In Progress', 'Resolved', 'Closed')
    - category: TEXT (e.g., 'Hardware', 'Software', 'Network')
    - subject: TEXT NOT NULL
    - description: TEXT
    - created_date: TEXT (format: YYYY-MM-DD)
    - resolved_date: TEXT
    - assigned_to: TEXT
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    cursor = conn.cursor()
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        priority TEXT CHECK(priority IN ('Critical', 'High', 'Medium', 'Low')),
        status TEXT DEFAULT 'Open' CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
        category TEXT CHECK(category IN ('Hardware', 'Software', 'Network')),
        subject TEXT NOT NULL,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ IT Tickets table created successfully!")

import streamlit as st
import pandas as pd
from datetime import datetime
from app.db import connect_database
from app.iticket import create_it_tickets_table

st.set_page_config(
    page_title="IT Tickets Management",
    page_icon="🎫",
    layout="wide",
)

st.title("🎫 IT Tickets Management")
st.caption("Track and resolve IT support tickets")

# ============= INITIALIZE DATABASE =============
@st.cache_resource
def init_tickets_table():
    """Initialize IT tickets table."""
    conn = connect_database()
    create_it_tickets_table(conn)
    conn.close()

try:
    init_tickets_table()
except Exception as e:
    st.error(f"Error initializing tickets table: {e}")

# ============= HELPER FUNCTIONS =============
@st.cache_data(ttl=60)
def load_tickets():
    """Load all IT tickets."""
    conn = connect_database()
    try:
        df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY created_at DESC", conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        st.error(f"Error loading tickets: {e}")
        return pd.DataFrame()

def insert_ticket(ticket_id, priority, status, category, subject, description, assigned_to=None):
    """Insert a new IT ticket."""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO it_tickets 
            (ticket_id, priority, status, category, subject, description, created_date, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, priority, status, category, subject, description, 
              datetime.now().strftime('%Y-%m-%d'), assigned_to))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_ticket_status(ticket_id, new_status, resolved_date=None):
    """Update ticket status."""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        if resolved_date:
            cursor.execute("""
                UPDATE it_tickets 
                SET status = ?, resolved_date = ?
                WHERE ticket_id = ?
            """, (new_status, resolved_date, ticket_id))
        else:
            cursor.execute("""
                UPDATE it_tickets 
                SET status = ?
                WHERE ticket_id = ?
            """, (new_status, ticket_id))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# ============= LOAD DATA =============
tickets_df = load_tickets()

# ============= KEY METRICS =============
st.header("📊 Ticket Overview")

if not tickets_df.empty:
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        total_tickets = len(tickets_df)
        st.metric("Total Tickets", total_tickets)
    
    with metric_col2:
        open_tickets = len(tickets_df[tickets_df['status'] == 'Open'])
        st.metric("Open Tickets", open_tickets)
    
    with metric_col3:
        critical_tickets = len(tickets_df[tickets_df['priority'] == 'Critical'])
        st.metric("Critical", critical_tickets, delta="High Priority", delta_color="inverse")
    
    with metric_col4:
        resolved_tickets = len(tickets_df[tickets_df['status'] == 'Resolved'])
        resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
        st.metric("Resolved", resolved_tickets, delta=f"{resolution_rate:.1f}%")
else:
    st.info("No tickets in the system yet.")

st.divider()

# ============= VISUALIZATIONS =============
st.header("📈 Analytics")

if not tickets_df.empty:
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Tickets by Priority")
        priority_counts = tickets_df['priority'].value_counts()
        st.bar_chart(priority_counts)
    
    with chart_col2:
        st.subheader("Tickets by Status")
        status_counts = tickets_df['status'].value_counts()
        st.bar_chart(status_counts)
    
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        st.subheader("Tickets by Category")
        category_counts = tickets_df['category'].value_counts()
        st.bar_chart(category_counts)
    
    with chart_col4:
        st.subheader("Resolution Rate by Category")
        category_resolution = tickets_df.groupby('category').apply(
            lambda x: (x['status'] == 'Resolved').sum() / len(x) * 100
        )
        st.bar_chart(category_resolution)

st.divider()

# ============= CREATE NEW TICKET =============
st.header("➕ Create New Ticket")

with st.form("new_ticket_form"):
    form_col1, form_col2 = st.columns(2)
    
    with form_col1:
        # Generate ticket ID
        ticket_count = len(tickets_df) if not tickets_df.empty else 0
        ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d')}-{ticket_count + 1:04d}"
        st.text_input("Ticket ID", value=ticket_id, disabled=True)
        
        priority = st.selectbox(
            "Priority",
            options=["Low", "Medium", "High", "Critical"]
        )
        
        category = st.selectbox(
            "Category",
            options=["Hardware", "Software", "Network"]
        )
        
        status = st.selectbox(
            "Status",
            options=["Open", "In Progress", "Resolved", "Closed"],
            index=0
        )
    
    with form_col2:
        subject = st.text_input(
            "Subject",
            placeholder="Brief description of the issue"
        )
        
        description = st.text_area(
            "Description",
            placeholder="Detailed description of the issue...",
            height=100
        )
        
        assigned_to = st.text_input(
            "Assigned To (Optional)",
            placeholder="Technician name"
        )
    
    submitted = st.form_submit_button("🚀 Create Ticket", type="primary")
    
    if submitted:
        if subject.strip() and description.strip():
            try:
                new_id = insert_ticket(
                    ticket_id=ticket_id,
                    priority=priority,
                    status=status,
                    category=category,
                    subject=subject,
                    description=description,
                    assigned_to=assigned_to if assigned_to.strip() else None
                )
                st.success(f"✅ Ticket {ticket_id} created successfully!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error creating ticket: {e}")
        else:
            st.warning("⚠️ Please provide both subject and description.")

st.divider()

# ============= UPDATE TICKET STATUS =============
st.header("🔄 Update Ticket Status")

if not tickets_df.empty:
    update_col1, update_col2, update_col3 = st.columns(3)
    
    with update_col1:
        ticket_to_update = st.selectbox(
            "Select Ticket",
            options=tickets_df['ticket_id'].tolist()
        )
    
    with update_col2:
        new_status = st.selectbox(
            "New Status",
            options=["Open", "In Progress", "Resolved", "Closed"],
            key="update_status"
        )
    
    with update_col3:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("💾 Update Status", type="primary"):
            try:
                resolved_date = datetime.now().strftime('%Y-%m-%d') if new_status == 'Resolved' else None
                rows_updated = update_ticket_status(ticket_to_update, new_status, resolved_date)
                if rows_updated > 0:
                    st.success(f"✅ Ticket {ticket_to_update} updated to {new_status}")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.warning("⚠️ Ticket not found")
            except Exception as e:
                st.error(f"❌ Error updating ticket: {e}")
else:
    st.info("No tickets available to update.")

st.divider()

# ============= TICKETS TABLE =============
st.header("📋 All Tickets")

if not tickets_df.empty:
    # Filters
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        priority_filter = st.multiselect(
            "Filter by Priority",
            options=tickets_df['priority'].unique(),
            default=None
        )
    
    with filter_col2:
        status_filter = st.multiselect(
            "Filter by Status",
            options=tickets_df['status'].unique(),
            default=None
        )
    
    with filter_col3:
        category_filter = st.multiselect(
            "Filter by Category",
            options=tickets_df['category'].unique(),
            default=None
        )
    
    with filter_col4:
        search_query = st.text_input("🔍 Search", placeholder="Search in subject...")
    
    # Apply filters
    filtered_df = tickets_df.copy()
    
    if priority_filter:
        filtered_df = filtered_df[filtered_df['priority'].isin(priority_filter)]
    
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    
    if category_filter:
        filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df['subject'].str.contains(search_query, case=False, na=False) |
            filtered_df['description'].str.contains(search_query, case=False, na=False)
        ]
    
    # Display table
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", width="small"),
            "ticket_id": st.column_config.TextColumn("Ticket ID", width="medium"),
            "priority": st.column_config.TextColumn("Priority", width="small"),
            "status": st.column_config.TextColumn("Status", width="small"),
            "category": st.column_config.TextColumn("Category", width="small"),
            "subject": st.column_config.TextColumn("Subject", width="medium"),
            "description": st.column_config.TextColumn("Description", width="large"),
            "created_date": st.column_config.DateColumn("Created"),
            "resolved_date": st.column_config.DateColumn("Resolved"),
            "assigned_to": st.column_config.TextColumn("Assigned To", width="small")
        }
    )
    
    # Export
    if st.button("📥 Export to CSV"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"it_tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
else:
    st.info("No tickets to display. Create your first ticket above!")

# ============= STATISTICS =============
if not tickets_df.empty:
    st.divider()
    st.header("📊 Detailed Statistics")
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.subheader("Priority Breakdown")
        priority_data = tickets_df['priority'].value_counts()
        for priority, count in priority_data.items():
            percentage = (count / len(tickets_df)) * 100
            st.write(f"**{priority}:** {count} ({percentage:.1f}%)")
    
    with stat_col2:
        st.subheader("Status Breakdown")
        status_data = tickets_df['status'].value_counts()
        for status, count in status_data.items():
            percentage = (count / len(tickets_df)) * 100
            st.write(f"**{status}:** {count} ({percentage:.1f}%)")
    
    with stat_col3:
        st.subheader("Category Breakdown")
        category_data = tickets_df['category'].value_counts()
        for category, count in category_data.items():
            percentage = (count / len(tickets_df)) * 100
            st.write(f"**{category}:** {count} ({percentage:.1f}%)")

# Footer
st.divider()
st.caption("💡 Data refreshes every 60 seconds. Create or update tickets to refresh immediately.")
