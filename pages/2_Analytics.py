import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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

from app.incidents import get_all_incidents

st.title("📈 Incident Analytics")

# Load real data
incidents_df = get_all_incidents()

# 1. Severity Distribution (Pie Chart)
st.subheader("📊 Incidents by Severity")
severity_counts = incidents_df['severity'].value_counts()
fig_pie = px.pie(
    values=severity_counts.values, 
    names=severity_counts.index, 
    title='Severity Distribution'
)
st.plotly_chart(fig_pie)

# 2. Category Distribution (Bar Chart)
st.subheader("📈 Incidents by Category")
category_counts = incidents_df['category'].value_counts()
fig_bar = px.bar(
    x=category_counts.index, 
    y=category_counts.values,
    labels={'x': 'Category', 'y': 'Count'},
    title='Incident Categories'
)
st.plotly_chart(fig_bar)
