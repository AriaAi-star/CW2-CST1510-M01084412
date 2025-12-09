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

# Page styling
st.markdown("""
<style>
    .contact-card {
        background: linear-gradient(135deg, #000000 0%, #333333 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }
    .info-card {
        background: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)
# title of the page 
st.title("📞 Contact Us")

# Header card
st.markdown("""
<div class='contact-card'>
    <h2 style='margin: 0; color: white;'>Get In Touch</h2>
    <p style='margin: 10px 0 0 0; color: rgba(255,255,255,0.9);'>We're here to help with your cybersecurity needs</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# About the Developer
st.markdown("### 👨‍💻 About the Developer")

col1, col2 = st.columns([1, 2])

with col1:
    # Display your photo (rotated 90 degrees clockwise)
    from PIL import Image
    img = Image.open("photo1.jpeg")
    img_rotated = img.rotate(-90,expand=True)  # -90 = 90 degrees clockwise. #i donnt know why but the photo neede rotation
    st.image(img_rotated, use_container_width=True, caption="Aria - Developer")

with col2:
    st.markdown("""
    <div class='info-card'>
        <h3 style='color: #000000; margin-top: 0;'>Aria - Platform Developer</h3>
        <p><strong style='color: #000000;'>Email:</strong> <span style='color: #000000;'>Ak2832@live.mdx.ac.uk</span></p>
        <p><strong style='color: #000000;'>Institution:</strong> <span style='color: #000000;'>Middlesex University London</span></p>
        <hr>
        <p style='margin-bottom: 0; color: #000000;'>
        This cybersecurity incident management platform was developed as part of the 
        CST 1510 coursework. The system provides comprehensive tools for monitoring, 
        analyzing, and managing security incidents with real-time data visualization 
        and AI-powered assistance.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Contact Information
st.markdown("### 📍 Contact Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='info-card' style='text-align: center;'>
        <h3 style='color: #000000; margin: 0;'>📧</h3>
        <h4 style='margin: 10px 0 5px 0;'>Email</h4>
        <p style='margin: 0; color: #000000;'>Ak2832@live.mdx.ac.uk</p>
        <p style='margin: 5px 0 0 0; color: #000000;'>Ak2832@live.mdx.ac.uk</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='info-card' style='text-align: center;'>
        <h3 style='color: #000000; margin: 0;'>📱</h3>
        <h4 style='margin: 10px 0 5px 0;'>Phone</h4>
        <p style='margin: 0; color: #000000;'>+44731009886</p>
        <p style='margin: 5px 0 0 0; color: #000000;'>Mon-Fri: 9AM - 6PM</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='info-card' style='text-align: center;'>
        <h3 style='color: #000000; margin: 0;'>📍</h3>
        <h4 style='margin: 10px 0 5px 0;'>Office</h4>
        <p style='margin: 0; color: #000000;'>NW9 5JA</p>
        <p style='margin: 5px 0 0 0; color: #000000;'>London, UK</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")



# FAQ Section
with st.expander("❓ Frequently Asked Questions"):
    st.markdown("""
    **Q: What are your support hours?**  
    A: We're available Monday to Friday, 9 AM to 6 PM (GMT).
    
    **Q: How quickly will I get a response?**  
    A: We aim to respond to all inquiries within 24 hours.
    
    **Q: Do you offer emergency support?**  
    A: Yes! For critical security incidents, please call our emergency hotline.
    
    **Q: Can I schedule a demo?**  
    A: Absolutely! Contact us to schedule a personalized demonstration.
    """)

st.info("💡 **Tip**: For urgent security incidents, please use the emergency contact number above.")
