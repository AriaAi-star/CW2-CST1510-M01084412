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

import streamlit as st
from datetime import datetime, date, time

st.set_page_config(
    page_title="Interactive Widgets",
    page_icon="🎛️",
    layout="wide",
)

st.title("Interactive Widgets")
st.caption("Adding user input to your application")

# Create three columns for organized layout
col1, col2, col3 = st.columns(3)

# ============= COLUMN 1: Text & Numeric =============
with col1:
    st.subheader("Text & Numeric")
    
    # Text input
    st.text_input("Write your text here")
    
    # Number input
    name = st.text_input("Name", value="John Doe")
    
    # Text area
    st.text_area("Feedback", placeholder="Type here...")
    
    # Number input
    age = st.number_input("Age", min_value=0, max_value=120, value=25)
    
    # Date input
    birth_date = st.date_input("Date of Birth", value=date(1990, 1, 1))
    
    # Time input
    meeting_time = st.time_input("Meeting Time", value=time(9, 0))

# ============= COLUMN 2: Selection =============
with col2:
    st.subheader("Selection")
    
    # Dropdown (single choice)
    dropdown_choice = st.selectbox(
        "Dropdown (single choice)",
        options=["Option 1", "Option 2", "Option 3"]
    )
    
    # Radio buttons (single choice)
    radio_choice = st.radio(
        "Radio buttons (single choice)",
        options=["Choice 1", "Choice 2", "Choice 3"]
    )
    
    # Multiselect
    multiselect_choices = st.multiselect(
        "Multiselect (multiple choices)",
        options=["Item A", "Item B", "Item C", "Item D"],
        default=["Item A"]
    )
    
    # Slider
    slider_value = st.slider("Slider", min_value=0, max_value=100, value=50)
    
    # Select slider
    select_slider_value = st.select_slider(
        "Select a value",
        options=["Low", "Medium", "High"],
        value="Medium"
    )

# ============= COLUMN 3: Actions =============
with col3:
    st.subheader("Actions")
    
    # Checkbox
    checkbox_state = st.checkbox("I agree to the terms")
    
    # Toggle
    toggle_state = st.toggle("Enable notifications")
    
    # Button
    if st.button("Submit"):
        st.success("Form submitted!")
    
    # Download button
    sample_data = "This is sample data for download"
    st.download_button(
        label="Download file",
        data=sample_data,
        file_name="sample.txt",
        mime="text/plain"
    )
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.info(f"Uploaded: {uploaded_file.name}")
    
    # Color picker
    color = st.color_picker("Pick a color", value="#FF5733")

# ============= Example Pattern Section =============
st.divider()
st.subheader("Example Pattern")

example_col1, example_col2 = st.columns(2)

with example_col1:
    st.code("""
name = st.text_input("Name")
st.write(name)
    """, language="python")

with example_col2:
    demo_name = st.text_input("Demo Name")
    if demo_name:
        st.write(f"Hello, {demo_name}!")

# ============= Display Current Values =============
st.divider()
st.subheader("Current Input Values")

values_col1, values_col2, values_col3 = st.columns(3)

with values_col1:
    st.write("**Text Inputs:**")
    st.write(f"Name: {name}")
    st.write(f"Age: {age}")
    st.write(f"Birth Date: {birth_date}")
    st.write(f"Meeting Time: {meeting_time}")

with values_col2:
    st.write("**Selections:**")
    st.write(f"Dropdown: {dropdown_choice}")
    st.write(f"Radio: {radio_choice}")
    st.write(f"Multiselect: {multiselect_choices}")
    st.write(f"Slider: {slider_value}")
    st.write(f"Select Slider: {select_slider_value}")

with values_col3:
    st.write("**Actions:**")
    st.write(f"Checkbox: {checkbox_state}")
    st.write(f"Toggle: {toggle_state}")
    st.write(f"Color: {color}")
    if uploaded_file:
        st.write(f"File: {uploaded_file.name}")

# Key Concept Widget values are returned immediately and can be stored in variables or used throughout your script.
st.info("💡 **Key Concept:** Widget values are returned immediately and can be stored in variables or used throughout your script.")
