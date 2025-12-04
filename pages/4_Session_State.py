import streamlit as st

# 🔒 Protected Page - Require Login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.info("Go to Home page to login")
    st.stop()

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
