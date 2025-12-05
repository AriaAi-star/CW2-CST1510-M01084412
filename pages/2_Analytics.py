import streamlit as st
import pandas as pd
import numpy as np
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

st.title("📈 Analytics")
st.write("This is Page 2")

# 1. Pie Chart (Circle Chart)
st.subheader("📊 Sales Distribution")
pie_data = pd.DataFrame({
    'Category': ['Product A', 'Product B', 'Product C', 'Product D'],
    'Value': [30, 25, 20, 25]
})
import plotly.express as px
fig_pie = px.pie(pie_data, values='Value', names='Category', title='Market Share')
st.plotly_chart(fig_pie)

# 2. Bar + Line Chart
st.subheader("📈 Revenue & Growth")
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
revenue = [45, 52, 48, 65, 70, 68]
growth = [10, 15, -8, 35, 8, -3]

fig = px.bar(x=months, y=revenue, labels={'x': 'Month', 'y': 'Revenue ($K)'})
fig.add_scatter(x=months, y=growth, name='Growth (%)', yaxis='y2', mode='lines+markers')
fig.update_layout(
    yaxis2=dict(overlaying='y', side='right', title='Growth (%)'),
    showlegend=True
)
st.plotly_chart(fig)
