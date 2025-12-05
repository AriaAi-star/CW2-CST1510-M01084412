import streamlit as st
from openai import OpenAI

# 🔒 Protected Page - Require Login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.info("Go to Home page to login")
    st.stop()

# AI Chatbot Sidebar
with st.sidebar:
    st.subheader("🤖 AI Assistant")
    user_msg = st.text_input("Ask me anything:")
    if st.button("Send") and user_msg:
        with st.spinner("Thinking..."):
            client = OpenAI(api_key="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")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_msg}]
            )
            st.success(response.choices[0].message.content)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.incidents import get_all_incidents

# Page Config
st.title("📊 Cyber Security Dashboard")

# Dashboard Customization Controls
st.markdown("### ⚙️ Customize Your Dashboard")
col1, col2, col3, col4 = st.columns(4)

with col1:
    severity_filter = st.multiselect(
        "🎯 Filter by Severity",
        options=['Critical', 'High', 'Medium', 'Low'],
        default=['Critical', 'High', 'Medium', 'Low'],
        help="Select severity levels to display"
    )

with col2:
    status_filter = st.multiselect(
        "📊 Filter by Status",
        options=['Open', 'In Progress', 'Resolved'],
        default=['Open', 'In Progress', 'Resolved'],
        help="Select incident status to display"
    )

with col3:
    category_filter = st.multiselect(
        "📦 Filter by Category",
        options=['Malware', 'Phishing', 'Data Breach', 'DDoS', 'Unauthorized Access', 'Ransomware'],
        default=['Malware', 'Phishing', 'Data Breach', 'DDoS', 'Unauthorized Access', 'Ransomware'],
        help="Select attack categories"
    )

with col4:
    view_limit = st.selectbox(
        "👁️ Show Records",
        options=[10, 25, 50, 100, 'All'],
        index=0,
        help="Number of incidents to display"
    )

st.markdown("---")

# Load real data
incidents_df = get_all_incidents()

# Apply filters
filtered_df = incidents_df.copy()

if severity_filter:
    filtered_df = filtered_df[filtered_df['severity'].isin(severity_filter)]

if status_filter:
    filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]

if category_filter:
    filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]

# Show filter results
if len(filtered_df) < len(incidents_df):
    st.info(f"📌 Showing **{len(filtered_df)}** of **{len(incidents_df)}** incidents based on your filters")

# Executive Summary
st.markdown("### 📋 Executive Summary")
total = len(filtered_df)
critical = len(filtered_df[filtered_df['severity'] == 'Critical'])
open_incidents = len(filtered_df[filtered_df['status'] == 'Open'])
resolved = len(filtered_df[filtered_df['status'] == 'Resolved'])
resolution_rate = (resolved / total * 100) if total > 0 else 0

st.info(f"""
**Overview**: The organization has recorded **{total} security incidents** to date. 
Currently, **{open_incidents} incidents remain open** requiring attention, while **{resolved} have been resolved** 
(resolution rate: **{resolution_rate:.1f}%**). Among active incidents, **{critical} are classified as Critical** 
and require immediate action.
""")

st.markdown("---")

# Real Stats with Colors
st.markdown("### 📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; text-align: center;'>
        <h2 style='color: white; margin: 0;'>{}</h2>
        <p style='color: white; margin: 5px 0 0 0;'>Total Incidents</p>
    </div>
    """.format(total), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 20px; border-radius: 10px; text-align: center;'>
        <h2 style='color: white; margin: 0;'>{}</h2>
        <p style='color: white; margin: 5px 0 0 0;'>🔥 Critical</p>
    </div>
    """.format(critical), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                padding: 20px; border-radius: 10px; text-align: center;'>
        <h2 style='color: white; margin: 0;'>{}</h2>
        <p style='color: white; margin: 5px 0 0 0;'>⚠️ Open</p>
    </div>
    """.format(open_incidents), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 20px; border-radius: 10px; text-align: center;'>
        <h2 style='color: white; margin: 0;'>{}</h2>
        <p style='color: white; margin: 5px 0 0 0;'>✅ Resolved</p>
    </div>
    """.format(resolved), unsafe_allow_html=True)

st.markdown("---")

# Charts Section
st.markdown("### 📊 Data Visualizations")

# Add chart type selector
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    chart_type = st.radio(
        "Select Chart Type:",
        options=["Donut Chart", "Bar Chart", "Pie Chart"],
        horizontal=True
    )

with chart_col2:
    color_scheme = st.selectbox(
        "Color Scheme:",
        options=["Pastel", "Bold", "Dark", "Ocean"],
        index=0
    )

# Color schemes
color_schemes = {
    "Pastel": px.colors.qualitative.Pastel,
    "Bold": px.colors.qualitative.Bold,
    "Dark": px.colors.qualitative.Dark24,
    "Ocean": px.colors.sequential.Blues
}

# Status Overview Chart
status_counts = filtered_df['status'].value_counts()

if chart_type == "Donut Chart":
    fig_status = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title='Incident Status Distribution',
        color_discrete_sequence=color_schemes[color_scheme],
        hole=0.4
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')
elif chart_type == "Bar Chart":
    fig_status = px.bar(
        x=status_counts.index,
        y=status_counts.values,
        title='Incident Status Distribution',
        labels={'x': 'Status', 'y': 'Count'},
        color=status_counts.index,
        color_discrete_sequence=color_schemes[color_scheme]
    )
else:  # Pie Chart
    fig_status = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title='Incident Status Distribution',
        color_discrete_sequence=color_schemes[color_scheme]
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig_status, use_container_width=True)

st.markdown("---")

# Show incidents with styling
num_to_show = view_limit if view_limit != 'All' else len(filtered_df)
st.markdown(f"### 🔴 Incident Records (Showing {num_to_show if view_limit != 'All' else 'All'})")

# Table display options
table_col1, table_col2 = st.columns([2, 1])

with table_col1:
    show_colors = st.checkbox("🎨 Color-code by Severity", value=True)

with table_col2:
    sort_by = st.selectbox(
        "Sort by:",
        options=['incident_id', 'timestamp', 'severity', 'status', 'category'],
        index=0
    )

# Add severity color coding
def highlight_severity(row):
    if row['severity'] == 'Critical':
        return ['background-color: #ffcccc'] * len(row)
    elif row['severity'] == 'High':
        return ['background-color: #ffe6cc'] * len(row)
    elif row['severity'] == 'Medium':
        return ['background-color: #ffffcc'] * len(row)
    else:
        return ['background-color: #ccffcc'] * len(row)

# Prepare display dataframe
display_df = filtered_df.sort_values(by=sort_by, ascending=False)
if view_limit != 'All':
    display_df = display_df.head(view_limit)

# Display table
if show_colors:
    st.dataframe(
        display_df.style.apply(highlight_severity, axis=1),
        use_container_width=True,
        height=400
    )
else:
    st.dataframe(display_df, use_container_width=True, height=400)

# Additional insights
st.markdown("---")
st.markdown("### 💡 Quick Insights")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    most_common_category = filtered_df['category'].mode()[0] if len(filtered_df) > 0 else 'N/A'
    category_count = filtered_df[filtered_df['category'] == most_common_category].shape[0]
    st.metric(
        "Most Common Attack",
        most_common_category,
        delta=f"{category_count} incidents"
    )

with insight_col2:
    most_common_severity = filtered_df['severity'].mode()[0] if len(filtered_df) > 0 else 'N/A'
    severity_count = filtered_df[filtered_df['severity'] == most_common_severity].shape[0]
    st.metric(
        "Most Common Severity",
        most_common_severity,
        delta=f"{severity_count} incidents"
    )

with insight_col3:
    open_percentage = (open_incidents / total * 100) if total > 0 else 0
    st.metric(
        "Open Rate",
        f"{open_percentage:.1f}%",
        delta=f"{open_incidents} active"
    )

# Download filtered data
st.markdown("---")
st.markdown("### 💾 Export Data")

csv = display_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name=f"incidents_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv",
)
