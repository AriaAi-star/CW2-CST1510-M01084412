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

st.title("📊 Dashboard")
st.write("This is Page 1")

st.info("Files in `pages/` folder become additional pages")

# Simple content
st.subheader("Quick Stats")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Users", "150")

with col2:
    st.metric("Sales", "$12,345")

with col3:
    st.metric("Growth", "23%", delta="5%")
