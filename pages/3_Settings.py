import streamlit as st

# 🔒 Protected Page - Require Login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.info("Go to Home page to login")
    st.stop()

st.title("⚙️ Settings")
st.write("This is Page 3")

st.info("Streamlit automatically creates navigation menu with page links")

# Simple form
st.subheader("User Preferences")
name = st.text_input("Name")
theme = st.selectbox("Theme", ["Light", "Dark"])

if st.button("Save"):
    st.success(f"Settings saved for {name}!")
