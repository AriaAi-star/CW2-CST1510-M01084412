import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from openai import OpenAI
import os

# 🔒 Protected Page - Require Login. 
#we have to make login mandotory for every singla page. 
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
            client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response=client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_msg}]
            )
            st.success(response.choices[0].message.content)


import plotly.graph_objects as go
from app.incidents import get_all_incidents
from datetime import datetime

st.title("📈 Security Analytics & Insights")
st.markdown("---")

# Load real data
incidents_df = get_all_incidents()

# Analytics Summary
st.markdown("### 🔍 Analytics Summary")
total = len(incidents_df)
most_common_category = incidents_df['category'].mode()[0] if len(incidents_df) > 0 else 'N/A'
most_common_severity = incidents_df['severity'].mode()[0] if len(incidents_df) > 0 else 'N/A'
category_count = incidents_df['category'].nunique()

st.success(f"""
**Key Findings**:  
✓ **Most Vulnerable Area**: {most_common_category} category has the highest incident count  
✓ **Risk Level**: {most_common_severity} severity incidents are most frequent  
✓ **Attack Vectors**: {category_count} different attack categories detected  
✓ **Sample Size**: Analysis based on {total} recorded incidents
""")

st.markdown("---")

# Two Column Layout
col1, col2 = st.columns(2)

with col1:
    # 1. Severity Distribution (Donut Chart)
    st.markdown("### 🎯 Severity Distribution")
    severity_counts =incidents_df['severity'].value_counts()
    
    colors = ['#FF6B6B',"#00EC72","#C41717",'#4ECDC4']
    fig_pie = px.pie(
        values=severity_counts.values, 
        names=severity_counts.index,
        title='Incidents by Severity Level',
        color_discrete_sequence=colors,
        hole=0.4
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}'
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Severity Insights
    critical_pct = (severity_counts.get('Critical', 0) / total * 100) if total > 0 else 0
    if critical_pct > 20:
        st.warning(f"⚠️ Critical incidents represent {critical_pct:.1f}% - immediate action required!")
    else:
        st.info(f"✓ Critical incidents at {critical_pct:.1f}% - within acceptable range")

with col2:
    # 2. Category Distribution (Bar Chart)
    st.markdown("### 📦 Category Breakdown")
    category_counts = incidents_df['category'].value_counts()
    
    fig_bar = px.bar(
        x=category_counts.values,
        y=category_counts.index,
        orientation='h',
        title='Incidents by Attack Category',
        labels={'x': 'Number of Incidents', 'y': 'Category'},
        color=category_counts.values,
        color_continuous_scale='Reds'
    )
    fig_bar.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Category Insights
    top_category=category_counts.index[0]
    top_count=category_counts.values[0]
    st.info(f"🎯 **Top Threat**: {top_category} with {top_count} incidents ({top_count/total*100:.1f}%)")

st.markdown("---")

# Status Comparison
st.markdown("### 📊 Resolution Performance")

status_counts=incidents_df['status'].value_counts()
fig_status=go.Figure(data=[
    go.Bar(
        x=status_counts.index,
        y=status_counts.values,
        text=status_counts.values,
        textposition='auto',
        marker=dict(
            color=['#FF6B6B', '#4ECDC4', '#95E1D3'],
            line=dict(color='rgb(8,48,107)', width=1.5)
        )
    )
])
fig_status.update_layout(
    title='Incident Status Overview',
    xaxis_title='Status',
    yaxis_title='Count',
    showlegend=False,
    height=350
)
st.plotly_chart(fig_status, use_container_width=True)

# Performance Metrics
resolved=status_counts.get('Resolved', 0)
open_count=status_counts.get('Open', 0)
resolution_rate=(resolved / total * 100) if total > 0 else 0

col1,col2,col3 = st.columns(3)
with col1:
    st.metric("Resolution Rate", f"{resolution_rate:.1f}%", delta="Target: 70%")
with col2:
    st.metric("Open Incidents", open_count, delta=f"-{resolved} resolved")
with col3:
    avg_per_category = total / category_count if category_count > 0 else 0
    st.metric("Avg per Category", f"{avg_per_category:.1f}")

st.markdown("---")

# Timeline Chart
st.markdown("### 📅 Incident Timeline")

# Convert timestamp to datetime if needed
incidents_df['timestamp'] = pd.to_datetime(incidents_df['timestamp'])
incidents_df['date'] = incidents_df['timestamp'].dt.date

# Count incidents per day
timeline_data = incidents_df.groupby('date').size().reset_index(name='count')

fig_timeline = px.line(
    timeline_data,
    x='date',
    y='count',
    title='Incidents Over Time',
    labels={'date': 'Date', 'count': 'Number of Incidents'},
    markers=True
)
fig_timeline.update_traces(
    line=dict(color='#667eea', width=3),
    marker=dict(size=8, color='#764ba2')
)
fig_timeline.update_layout(
    hovermode='x unified',
    height=400
)
st.plotly_chart(fig_timeline, use_container_width=True)

st.markdown("---")

# Combined View
st.markdown("### 🔄 Severity vs Status Matrix")

matrix = pd.crosstab(incidents_df['severity'], incidents_df['status'])
fig_heatmap = px.imshow(
    matrix,
    labels=dict(x="Status", y="Severity", color="Count"),
    title="Incident Distribution Matrix",
    color_continuous_scale='RdYlGn_r',
    text_auto=True
)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")
st.markdown("#### 💡 **Recommendations**")
st.markdown(f"""
- Focus on resolving **{open_count} open incidents** to improve resolution rate
- Strengthen defenses against **{most_common_category}** attacks (highest frequency)
- Prioritize **{severity_counts.get('Critical', 0)} critical incidents** for immediate response
- Consider additional security measures for top {min(3, category_count)} attack vectors
""")
