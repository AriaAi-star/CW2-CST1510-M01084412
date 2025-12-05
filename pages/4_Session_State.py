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

st.title("Session State Demo")

# 1. Initialization Pattern
if "count" not in st.session_state:
    st.session_state.count = 0

if "name" not in st.session_state:
    st.session_state.name = ""

# 2. Reading and Writing
st.subheader("Counter Example")

col1, col2 = st.columns(2)

with col1:
    if st.button("Increment"):
        st.session_state.count += 1

with col2:
    if st.button("Reset"):
        st.session_state.count = 0

st.write(f"Count: {st.session_state.count}")

st.divider()

# Name input example
st.subheader("Name Example")
st.session_state.name = st.text_input("Enter your name", st.session_state.name)
if st.session_state.name:
    st.write(f"Hello, {st.session_state.name}!")

st.divider()

# Show all session state
st.subheader("Current Session State")
st.write(st.session_state)
