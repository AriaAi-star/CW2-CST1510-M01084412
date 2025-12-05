import streamlit as st
import os
from dotenv import load_dotenv
from app.users import hash_password, password_verification

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Security Platform Login", 
    page_icon="🔐",
    layout="centered"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    div[data-testid="stMarkdownContainer"] h1 {
        color: white;
        text-align: center;
        padding: 20px;
        font-size: 3em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .login-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        margin: 20px auto;
        max-width: 500px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 15px;
        border: none;
        font-size: 16px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .welcome-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 20px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🔐 Cyber Security Platform</h1>", unsafe_allow_html=True)

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
    # Add a welcome message
    st.markdown("""
    <div style='text-align: center; color: white; padding: 20px;'>
        <h3 style='color: white;'>Welcome to the Intelligent Security Platform</h3>
        <p style='color: rgba(255,255,255,0.9);'>Secure access to your incident management dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create centered container for login/register
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        # Login tab
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Sign in to your account")
            username = st.text_input("👤 Username", key="login_user", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", key="login_pass", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 Sign In"):
                if username in st.session_state.users:
                    stored_hash = st.session_state.users[username]
                    if password_verification(password, stored_hash):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("✅ Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.error("❌ Invalid username or password")
    
        # Register tab
        with tab2:
            import string
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Create new account")
            new_user = st.text_input("👤 Username", key="reg_user", placeholder="Choose a username")
            new_pass = st.text_input("🔒 Password", type="password", key="reg_pass", placeholder="Create a strong password")
            confirm_pass = st.text_input("🔒 Confirm Password", type="password", key="reg_confirm", placeholder="Re-enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("✨ Create Account"):
                # Check if username exists
                if new_user in st.session_state.users:
                    st.error("❌ Username already exists")
                elif new_pass != confirm_pass:
                    st.error("❌ Passwords don't match")
                elif not new_user or not new_pass:
                    st.warning("⚠️ Please fill all fields")
                else:
                    # Password validation
                    errors = []
                    
                    # Check length
                    if len(new_pass) <= 8:
                        errors.append("❌ Password must be more than 8 characters")
                    else:
                        st.success("✅ Good job! Your password has required minimum length")
                    
                    # Check uppercase
                    has_upper = any(c.isupper() for c in new_pass)
                    if has_upper:
                        st.success("✅ Nice! Your password has uppercase letter")
                    else:
                        errors.append("❌ Your password doesn't have uppercase")
                    
                    # Check lowercase
                    has_lower = any(c.islower() for c in new_pass)
                    if has_lower:
                        st.success("✅ Nice! Your password has lowercase letter")
                    else:
                        errors.append("❌ Your password doesn't have lowercase")
                    
                    # Check digit
                    has_digit = any(c.isdigit() for c in new_pass)
                    if has_digit:
                        st.success("✅ Nice! Your password has digit")
                    else:
                        errors.append("❌ Your password doesn't have digit")
                    
                    # Check space
                    has_space = any(c.isspace() for c in new_pass)
                    if has_space:
                        errors.append("❌ Your password has space. Please remove it")
                    else:
                        st.success("✅ Nice! Your password doesn't have space")
                    
                    # Check special character
                    has_special = any(c in string.punctuation for c in new_pass)
                    if has_special:
                        st.success("✅ Nice! Your password has special character")
                    else:
                        errors.append("❌ Your password doesn't have special character")
                    
                    # If all validations pass
                    if not errors:
                        hashed = hash_password(new_pass)
                        st.session_state.users[new_user] = hashed
                        save_user(new_user, new_pass)
                        st.success("🎉 Registration successful! Password is secure and hashed. Please login.")
                    else:
                        for error in errors:
                            st.error(error)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Logged in view
else:
    # Welcome card with gradient
    st.markdown(f"""
    <div class='welcome-card'>
        <h2 style='margin: 0; color: white;'>🎉 Welcome Back!</h2>
        <h3 style='margin: 10px 0; color: white;'>{st.session_state.username}</h3>
        <p style='margin: 0; color: rgba(255,255,255,0.9);'>You are successfully logged in</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card' style='text-align: center;'>
            <h3 style='color: #667eea; margin: 0;'>✅</h3>
            <h4 style='margin: 5px 0;'>Status</h4>
            <p style='color: #4CAF50; font-weight: bold; margin: 0;'>Logged In</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center;'>
            <h3 style='color: #667eea; margin: 0;'>👤</h3>
            <h4 style='margin: 5px 0;'>User</h4>
            <p style='color: #667eea; font-weight: bold; margin: 0;'>{st.session_state.username}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card' style='text-align: center;'>
            <h3 style='color: #667eea; margin: 0;'>🔐</h3>
            <h4 style='margin: 5px 0;'>Security</h4>
            <p style='color: #4CAF50; font-weight: bold; margin: 0;'>Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation info
    st.info("🎯 Navigate to other pages using the sidebar ← to access Dashboard, Analytics, Settings, and more!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Center the logout button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun() 