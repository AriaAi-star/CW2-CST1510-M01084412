import streamlit as st
from openai import OpenAI
import os

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
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_msg}]
            )
            st.success(response.choices[0].message.content)

st.title("⚙️ Settings")

st.markdown("### 👤 User Preferences")

# User settings
col1, col2 = st.columns(2)

with col1:
    st.text_input("Email", value=f"{st.session_state.username}@company.com", disabled=True)
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    
with col2:
    st.text_input("Username", value=st.session_state.username, disabled=True)
    language = st.selectbox("Language", ["English", "Farsi", "Arabic"])

st.markdown("---")

st.markdown("### 🔔 Notification Settings")

col1, col2 = st.columns(2)

with col1:
    email_notif = st.checkbox("Email Notifications", value=True)
    critical_alerts = st.checkbox("Critical Alerts", value=True)
    
with col2:
    push_notif = st.checkbox("Push Notifications", value=False)
    weekly_report = st.checkbox("Weekly Reports", value=True)

st.markdown("---")

st.markdown("### 🔐 Security Settings")

col1, col2 = st.columns(2)

with col1:
    two_factor = st.checkbox("Two-Factor Authentication", value=False)
    session_timeout = st.selectbox("Session Timeout", ["15 minutes", "30 minutes", "1 hour", "4 hours"])
    
with col2:
    login_alerts = st.checkbox("Login Alerts", value=True)
    ip_whitelist = st.checkbox("IP Whitelist", value=False)

st.markdown("---")

st.markdown("### 📊 Dashboard Settings")

show_summary = st.checkbox("Show Executive Summary", value=True)
default_view = st.selectbox("Default View", ["Dashboard", "Analytics"])
items_per_page = st.slider("Items per page", 5, 100, 10)

st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("💾 Save Changes", use_container_width=True):
        st.success("✅ Settings saved successfully!")
        
with col2:
    if st.button("🔄 Reset to Default", use_container_width=True):
        st.info("⚠️ Settings reset to default values")
        
with col3:
    if st.button("❌ Cancel", use_container_width=True):
        st.info("Changes discarded")
