### setup
import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb

from dotenv import load_dotenv
from model import *
load_dotenv()

import os

from sqlalchemy import select, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from sqlalchemy.ext.automap import automap_base
from ml import MLModel

mlwrapper = MLModel()

SERVER = os.getenv('SERVER')
DATABASE = os.getenv('DATABASE')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
DRIVER = os.getenv('DRIVER')

conn_settings = ConnectionSettings(
    server=SERVER, 
    database=DATABASE, 
    username=USERNAME, 
    password=PASSWORD,
    driver=DRIVER)


db_conn = AzureDbConnection(conn_settings)



st.title('DB Final Project part 4')
### Dummy data for development part
sample = {'id': 111, 'age': 63, 'sex': 'Male', 'dataset': 'Cleveland', 'cp':'typical angina',
          'trestbps': 145.0, 'chol': 233.0, 'fbs': True, 'restecg': 'lv hypertrophy', 'thalch': 150.0,
          'exang': False, 'oldpeak': 2.3, 'slope': 'downsloping', 'ca': 0.0, 'thal': 'fixed defect',
          'num': 0, 'Job': 2, 'Housing': 'own', 'SavingAccounts': None, 'CheckingAccount': None, 
          'CreditAmount': 5943, 'Duration': 24, 'Purpose': 'radio/TV', 'bmi': 39.16, 'children': 1,
          'smoker': 'no', 'region': 'southeast', 'charges': 14418.2804}




st.markdown("## Upload New customers information")
# upload data from csv 
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

## Separate Dataset into our requirements


## Upload database on azure
st.markdown("### Upload Data into Database")
if st.button("Upload", type="primary"):
    # produce our own MetaData object
    metadata = MetaData()

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare(db_conn.engine(), reflect=True)

    session = db_conn.session()
    credit_i = Credit(Id=sample['id'], Job=sample['Job'], Housing=sample['Housing'], SavingAccounts=sample['SavingAccounts'],
                      CheckingAccount=sample['CheckingAccount'], CreditAmount=sample['CreditAmount'],
                      Duration=sample['Duration'], Purpose=sample['Purpose'])
    insurance_i = Insurance(Id=sample['id'], bmi=sample['bmi'], children=sample['children'], smoker=sample['smoker'],
                      region=sample['region'], charges=sample['charges'])
    heart_i = Heart(id=sample['id'], age=sample['age'], sex=sample['sex'], dataset=sample['dataset'],
                      cp=sample['cp'], trestbps=sample['trestbps'], chol=sample['chol'], fbs=sample['fbs'],
                      restecg=sample['restecg'], thalch=sample['thalch'], exang=sample['exang'], oldpeak=sample['oldpeak'],
                      slope=sample['slope'], ca=sample['ca'], thal=sample['thal'], num=sample['num'])
    session.add(credit_i)
    session.add(insurance_i)
    session.add(heart_i)
    session.commit()
    session.close()
    
    
st.markdown("### Show something results")

## ML Model response
st.markdown("### Prediction heart disease risk")
if st.button("Prediction", type="primary"):
    # produce our own MetaData object
    metadata = MetaData()

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare(db_conn.engine(), reflect=True)

    session = db_conn.sessionMaker()
    # Return table or csv files
    mlwrapper.preprocess(sample)
    res, pred = mlwrapper.prediction()
    st.markdown(f"### This customer has {res}")
    query = session.query(Heart).where(Heart.num==sample['num'])
    
    query.num = pred
    session.commit()
    session.close()


## Retrain Models
st.markdown("### Retrain heart disease risk model")
if st.button("Retrain", type="primary"):
    # Extract data from dbs
    # produce our own MetaData object
    metadata = MetaData()

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare(db_conn.engine(), reflect=True)

    session = db_conn.sessionMaker()
    # heart_i = session.query(Heart).all()
    # insurance_i = session.query(Insurance).all()
    # credit_i = session.query(Credit).all()
    h = pd.read_sql(sql="select * from Heart", con=db_conn.engine())
    i = pd.read_sql(sql="select * from Insurance", con=db_conn.engine())
    c = pd.read_sql(sql="select * from Credit", con=db_conn.engine())
    

    df = pd.concat([h, c, i])
    # preprocess
    mlwrapper.preprocess_retrain(df)
    # retrain
    mlwrapper.retrain()
    st.markdown(f"### Finished retraining and save new model")
    session.close()

