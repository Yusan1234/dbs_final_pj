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

## Separate Dataset into our requirements


## Upload database on azure
st.markdown("### Upload Data into Database")
target = False
target = st.radio("Choose upload a table",
    ["Customer", "Account", "Product", "CompanyCode", "Credit", "Heart", "Insurance"])

# upload data from csv
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
if st.button("Upload", type="primary"):
    if not target:
        st.markdown("### Error")
        
    else:
        # produce our own MetaData object
        metadata = MetaData()

        # we can then produce a set of mappings from this MetaData.
        Base = automap_base(metadata=metadata)

        # calling prepare() just sets up mapped classes and relationships.
        Base.prepare(db_conn.engine(), reflect=True)

        session = db_conn.session()

        if target=='Account':
            Account = Base.classes.Account
            h = pd.read_sql(sql="select * from Account", con=db_conn.engine())
            AList = h['AccountID'].to_list()
            for i, val in df.iterrows():# df shape
                if str(val['AccountID']) in AList:
                    continue
                print(val)
                print(AList)
                account_i = Account(AccountID=val['AccountID'], AccountName=val['AccountName'], AccountName2=val['AccountName2'], 
                    LocationAddress1=val['LocationAddress1'], LocationAddress2=val['LocationAddress2'], LocationCity=val['LocationCity'],
                    LocationState=val['LocationState'], LocationZip=val['LocationZip'], CompanyCode=val['CompanyCode'])

                session.add(account_i)
        
        elif target=='Product':
            Product = Base.classes.Product
            h = pd.read_sql(sql="select * from Product", con=db_conn.engine())
            ProductList = h['LineOfBusiness'].to_list()
            for i, val in df.iterrows():# df shape
                if val['LineOfBusiness'] in ProductList:
                    continue
                product_i = Product(LineOfBusiness=val['LineOfBusiness'], ProductDescription=val['Description'])
                session.add(product_i)
        
        elif target=='Customer':
            Customer = Base.classes.Customer
            h = pd.read_sql(sql="select * from Customer", con=db_conn.engine())
            CodeList = h['CustID'].to_list()
            for i, val in df.iterrows():# df shape
                if str(val['CustID']) in CodeList:
                    continue
                customer_i = Customer(CustID=val['CustID'], CustFirstName=val['CustFirstName'], CustMiddleInitial=val['CustMiddleInitial'],
                    CustLastName=val['CustLastName'], CustSuffix=val['CustSuffix'], CustDOB=val['CustDOB'], Gender=val['Gender'])
                session.add(customer_i)

        
        elif target=="CompanyCode":
            CompanyCode = Base.classes.CompanyCode
            h = pd.read_sql(sql="select * from CompanyCode", con=db_conn.engine())
            CodeList = h['CompanyCode'].to_list()
            for i, val in df.iterrows():# df shape
                if str(val['CompanyCode']) in CodeList:
                    continue
                company_i = CompanyCode(CompanyCode=val['CompanyCode'], CompanyName=val['CompanyName'])
                session.add(company_i)

        elif target=='Credit':
            Credit = Base.classes.Credit
            h = pd.read_sql(sql="select * from Credit", con=db_conn.engine())
            
            pids = []
            pids = h['Id'].to_list()
            for i, val in df.iterrows():# df shape
                if str(val['Id']) in pids:
                    continue
                credit_i = Credit(Id=val['Id'], Job=val['Job'], Housing=val['Housing'], SavingAccounts=val['Saving accounts'],
                    CheckingAccount=val['Checking account'], CreditAmount=val['Credit amount'],
                    Duration=val['Duration'], Purpose=val['Purpose'])
                session.add(credit_i)
                
        elif target=='Insurance':
            Insurance = Base.classes.Insurance
            h = pd.read_sql(sql="select * from Insurance", con=db_conn.engine())
            pids = []
            pids = h['Id'].to_list()
            for i, val in df.iterrows():# df shape
                if str(val['Id']) in pids:
                    continue
                insurance_i = Insurance(Id=val['Id'], bmi=val['bmi'], children=val['children'], smoker=val['smoker'],
                            region=val['region'], charges=val['charges'])
                session.add(insurance_i)
        
        elif target=='Heart':
            heart = Base.classes.heart
            h = pd.read_sql(sql="select * from heart", con=db_conn.engine())
            pids = h['id'].to_list()
            pids = []
            for i, val in df.iterrows():# df shape
                if str(val['id']) in pids:
                    continue
                heart_i = heart(id=val['id'], age=val['age'], sex=val['sex'], dataset=val['dataset'],
                    cp=val['cp'], trestbps=val['trestbps'], chol=val['chol'], fbs=val['fbs'],
                    restecg=val['restecg'], thalch=val['thalch'], exang=val['exang'], oldpeak=val['oldpeak'],
                    slope=val['slope'], ca=val['ca'], thal=val['thal'], num=val['num'])
                session.add(heart_i)

        session.commit()
        session.close()
        st.markdown("### Upload Succeeded")
## Upload database on azure
st.markdown("### Search An Account info")

AccountName = st.text_input("Insert an Account Name", value=None, placeholder="Type a name...")
if st.button("Search", type='primary'):
    # produce our own MetaData object
    metadata = MetaData()

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare(db_conn.engine(), reflect=True)

    session = db_conn.sessionMaker()


    Account = Base.classes.Account
    h = pd.read_sql(sql="select * from Account", con=db_conn.engine())
    print(h)
    h = h[h['AccountName']==AccountName]
    st.dataframe(data=h)
    
    session.close()
    st.markdown("### Search Succeeded")
    
st.markdown("### Update An Account info")
target_update = st.radio("Choose update a column in Account table",
    ["AccountName", "AccountName2", "LocationAddress1", "LocationAddress2", "LocationCity", "LocationState",
     "LocationZip"])
Name = st.text_input("Insert an Account Name for Search", value=None, placeholder="Type a name...")
NewData = st.text_input("Insert an New Data for Update", value=None, placeholder="Type new data...")
if st.button("Update", type='primary'):
    # produce our own MetaData object
    metadata = MetaData()

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare(db_conn.engine(), reflect=True)

    session = db_conn.sessionMaker()


    # Account = Base.classes.Account
    # query = session.query(Account).where(Account.AccountName==Name)
    if not NewData or not Name:
        st.markdown("### Search Failed/New Data is a blank")
    if target_update=="AccountName":
        stmt = (
            select(Account)
            .where(Account.AccountName == Name)
        )
        a = session.scalars(stmt).one()
        a.AccountName = NewData

    elif target_update=="AccountName2":
        # query.AccountName2 = NewData
        # session.add(query)
        # print(query.AccountName2)
        stmt = (
            select(Account)
            .where(Account.AccountName == Name)
        )
        a = session.scalars(stmt).one()
        a.AccountName2 = NewData

    elif target_update=="LocationAddress1":
        stmt = (
            select(Account)
            .where(Account.AccountName == Name)
        )
        a = session.scalars(stmt).one()
        a.LocationAddress1 = NewData
        
        
    elif target_update=="LocationAddress2":
        stmt = (
            select(Account)
            .where(Account.AccountName == Name)
        )
        a = session.scalars(stmt).one()
        a.LocationAddress2 = NewData
    elif target_update=="LocationCity":
        stmt = (
            select(Account)
            .where(Account.AccountName == Name)
        )
        a = session.scalars(stmt).one()
        a.LocationCity = NewData
    elif target_update=="LocationState":
        stmt = (
            select(Account)
            .where(Account.AccountName == Name)
        )
        a = session.scalars(stmt).one()
        a.LocationState = NewData
    elif target_update=="LocationZip":
        stmt = (
            select(Account)
            .where(Account.AccountName == Name)
        )
        a = session.scalars(stmt).one()
        a.LocationZip = NewData
        
    session.commit()
    session.close()
    st.markdown("### Update Succeeded")
    
AccountName = st.text_input("Insert an AccountName", value=None, placeholder="Type an ID...")
if st.button("Delete", type='primary'):
    # produce our own MetaData object
    metadata = MetaData()

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare(db_conn.engine(), reflect=True)

    session = db_conn.sessionMaker()

    Account = Base.classes.Account
    query = session.query(Account).where(Account.AccountName==AccountName)
    query.delete()
    session.commit()
    session.close()
    h = pd.read_sql(sql="select * from Account", con=db_conn.engine())
    h = h[h['AccountName']==AccountName]
    st.dataframe(data=h)
    st.markdown("### Delete Succeeded")

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
    heart = Base.classes.heart
    # Return table or csv files
    h = pd.read_sql(sql="select * from heart", con=db_conn.engine())
    i = pd.read_sql(sql="select * from Insurance", con=db_conn.engine())
    c = pd.read_sql(sql="select * from Credit", con=db_conn.engine())
    c = c.rename(columns={"Id":"id"})
    i = i.rename(columns={"Id":"id"})
    h = h.rename(columns={"Id":"id"})
    c = c.drop('id', axis=1)
    i = i.drop('id', axis=1)
    df = pd.concat([h, c, i], axis=1)
    
    
    mlwrapper.preprocess(df)
    res = mlwrapper.prediction()
    for idx, val in res.iterrows():
        query = session.query(heart).where(heart.id==val['id'])
        query.num = val['pred']
        session.commit()
    h = pd.read_sql(sql="select * from heart", con=db_conn.engine())
    h = h[['id', 'num']]
    h.to_csv('a.csv')
    session.close()
    st.markdown(f"### Updated Prediction Results")
    with open('a.csv') as f:
        st.download_button('Download Prediction Results', f)


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
    h = pd.read_sql(sql="select * from heart", con=db_conn.engine())
    i = pd.read_sql(sql="select * from Insurance", con=db_conn.engine())
    c = pd.read_sql(sql="select * from Credit", con=db_conn.engine())
    c = c.rename(columns={"Id":"id"})
    i = i.rename(columns={"Id":"id"})
    h = h.rename(columns={"Id":"id"})
    c = c.drop('id', axis=1)
    i = i.drop('id', axis=1)
    df = pd.concat([h, c, i], axis=1)
    # preprocess
    mlwrapper.preprocess_retrain(df)
    # retrain
    mlwrapper.retrain()
    st.markdown(f"### Finished retraining and save new model")
    session.close()

