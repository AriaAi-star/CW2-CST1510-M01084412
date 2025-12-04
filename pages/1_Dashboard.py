import streamlit as st

# 🔒 Protected Page - Require Login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.info("Go to Home page to login")
    st.stop()

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
