import streamlit as st
from openai import OpenAI
import os

#WE HAVE TO MAKE LOHIN MANDOTORY.
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.info("Go to Home page to login")
    st.stop()

# AI Chatbot Sidebar.
# WE HAVE THE SAME CODE FOR ALL OF THE PAGES.
with st.sidebar:
    st.subheader("🤖 AI Assistant")
    user_msg = st.text_input("Hi dear, I am your AI assistant.Ask me whatever you want")
    if st.button("Send") and user_msg:
        with st.spinner("Thinking..."):
            client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response=client.chat.completions.create(
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

view_limit=st.selectbox(
    "👁️ Show Records",
    options=[10, 25, 50, 100, 'All'],
    index=0,
    help="Number of incidents to display"
)

st.markdown("---")

# Load real data
incidents_df=get_all_incidents()
filtered_df=incidents_df.copy()

# Executive Summary
st.markdown("### 📋 Executive Summary")
total=len(filtered_df)
critical=len(filtered_df[filtered_df['severity']=='Critical'])
open_incidents=len(filtered_df[filtered_df['status']=='Open'])
resolved=len(filtered_df[filtered_df['status']=='Resolved'])
resolution_rate=(resolved / total * 100) if total > 0 else 0

st.info(f""" **overview**: 
The organization has reported a total of **{total}** security incidents thus far.
 At present, there are **{open_incidents}** active incidents requiring action,
 while **{resolved}** incidents have been resolved (the resolution rate is **{resolution_rate:.1f}** percent).
Of the active incidents, there are **{critical}** rated critical and needing immediate attention.

""")




st.markdown("---")

# Real Stats with Colors
st.markdown("### 📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
#designing the boxes
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

chart_type=st.radio(
    "Select Chart Type:",
    options=["Donut Chart", "Bar Chart", "Pie Chart"],
    horizontal=True
)

#we can give the opprotuinity to  choose to see that tehy wannaa see the data in what type
status_counts = filtered_df['status'].value_counts()

if chart_type=="Donut Chart":
    fig_status=px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title='Incident Status Distribution',
        hole=0.4
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')
elif chart_type == "Bar Chart":
    fig_status = px.bar(
        x=status_counts.index,
        y=status_counts.values,
        title='Incident Status Distribution',
        labels={'x': 'Status', 'y': 'Count'},
        color=status_counts.index
    )
else:  # Pie Chart
    fig_status=px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title='Incident Status Distribution'
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig_status, use_container_width=True)

st.markdown("---")

# Show incidents with styling
num_to_show=view_limit if view_limit != 'All' else len(filtered_df)
st.markdown(f"### 🔴 Incident Records (Showing {num_to_show if view_limit != 'All' else 'All'})")

# Prepare display dataframe
display_df = filtered_df
if view_limit != 'All':
    display_df = display_df.head(view_limit)

# Display table
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
