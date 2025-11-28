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
    st.subheader("Dataset Rows")
    st.bar_chart(data.set_index('name')['rows'])

with col2:
    st.subheader("Dataset Columns")
    st.bar_chart(data.set_index('name')['columns'])


with st.expander("Show raw data"):
    st.write(data)