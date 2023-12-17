import sqlalchemy as sqla
import streamlit as st
# Function to connect to the database

def connect_db():
    # Set up a connection string
    username = st.secrets['user']
    password = st.secrets['pw']
    host = 'dmsfall2023.database..windows.com'
    database = 'dbAdmin'
    port = '5432'  # or your specified port number
    conn_str = f"postgresql://{username}:{password}@{host}:{port}/{database}?"
    return conn_str