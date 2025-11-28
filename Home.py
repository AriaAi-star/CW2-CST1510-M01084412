import streamlit as st
from app.metadata import get_all_datasets_metadata
from app.db import connect_database

conn = connect_database()
data = get_all_datasets_metadata(conn)
conn.close()


st.set_page_config(
    page_title="Data Explorer App",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Data Explorer App")

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This app visualizes datasets metadata from the database.
        """
    )
    st.selectbox(
        "Select Dataset Category",
        options=data['dataset_id'].unique()
    )


col1 , col2 = st.columns(2)

with col1:
    st.subheader("1st chart")
    st.bar_chart(x='name', y='rows', data=data)

with col2:
    st.subheader("2nd chart")
    st.line_chart(x='uploaded_by', y='columns', data=data)


with st.expander("Show raw data"):
    st.write(data)