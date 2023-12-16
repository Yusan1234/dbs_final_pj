### setup
import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb

model_init = xgb.Booster()
model_init.load_model("model.json")


st.title('DB Final Project part 4')
###


st.markdown("## Upload New customers information")
# upload data from csv 
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

## Separate Dataset into our requirements


## Upload database on azure
st.markdown("### Upload Data into Database")
if st.button("Upload", type="primary"):
    
    print('a')

st.markdown("### Show something results")

## ML Model response
st.markdown("### Prediction heart disease risk")
if st.button("Prediction", type="primary"):
    # Return table or csv files
    print('a')

## Retrain Models
st.markdown("### Retrain heart disease risk model")
if st.button("Retrain", type="primary"):
    # Extract data from dbs
    # preprocess
    # retrain
    
    print('a')
    

