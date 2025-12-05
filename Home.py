import streamlit as st
import os
from app.users import hash_password, password_verification

st.set_page_config(page_title="My App", page_icon="🔐")

st.title("🔐 Authentication System")

USER_FILE = "DATA/user.txt"

# Load users from file
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if ',' in line:
                    username, password_hash = line.split(',', 1)
                    users[username] = password_hash
    return users

# Save user to file with hashed password
def save_user(username, password):
    hashed = hash_password(password)
    with open(USER_FILE, 'a') as f:
        f.write(f"{username},{hashed}\n")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "users" not in st.session_state:
    st.session_state.users = load_users()

# Not logged in - show login/register
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    # Login tab
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            if username in st.session_state.users:
                stored_hash = st.session_state.users[username]
                if password_verification(password, stored_hash):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Invalid username or password")
    
    # Register tab
    with tab2:
        new_user = st.text_input("Username", key="reg_user")
        new_pass = st.text_input("Password", type="password", key="reg_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register"):
            if new_user in st.session_state.users:
                st.error("Username already exists")
            elif new_pass != confirm_pass:
                st.error("Passwords don't match")
            elif new_user and new_pass:
                hashed = hash_password(new_pass)
                st.session_state.users[new_user] = hashed
                save_user(new_user, new_pass)  # Save to file (will be hashed inside)
                st.success("✅ Registration successful! Password hashed with bcrypt + salt. Please login.")
            else:
                st.warning("Please fill all fields")

# Logged in view
else:
    st.success(f"✅ Welcome, {st.session_state.username}!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Status", "Logged In")
    with col2:
        st.metric("User", st.session_state.username)
    
    st.info("Navigate to other pages using the sidebar ←")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
