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
from app.incidents import get_all_incidents

st.title("📊 Cyber Incidents Dashboard")

# Load real data
incidents_df = get_all_incidents()

# Real Stats
st.subheader("📈 Real-Time Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Incidents", len(incidents_df))

with col2:
    critical = len(incidents_df[incidents_df['severity'] == 'Critical'])
    st.metric("Critical", critical, delta=f"{critical} urgent")

with col3:
    open_incidents = len(incidents_df[incidents_df['status'] == 'Open'])
    st.metric("Open", open_incidents)

with col4:
    resolved = len(incidents_df[incidents_df['status'] == 'Resolved'])
    st.metric("Resolved", resolved)

# Show recent incidents
st.subheader("🔴 Recent Incidents")
st.dataframe(incidents_df.head(10), use_container_width=True)
