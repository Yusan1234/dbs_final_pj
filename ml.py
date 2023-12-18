import xgboost as xgb
import pandas as pd
import os 
class MLModel:
    def __init__(self):
        self.model = xgb.XGBClassifier()
    
    def preprocess(self, data:dict):
        
        self.model.load_model('model.json')
        df = pd.DataFrame(data, index=[0])
        df = df.rename(columns={'SavingAccounts':'Saving accounts', 'CheckingAccount':'Checking account', 'CreditAmount':'Credit amount'})
        cat_cols = []
        for c, v in zip(df.columns, df.dtypes):
            if v=='object':
                cat_cols.append(c)

        for col in cat_cols:
            df[col] = df[col].astype('category')
            
        
        self.tr = df.drop('num', axis=1)
        self.te = df['num']
    def preprocess_retrain(self, df):
        df = df.rename(columns={'SavingAccounts':'Saving accounts', 'CheckingAccount':'Checking account', 'CreditAmount':'Credit amount'})
        cat_cols = []
        for c, v in zip(df.columns, df.dtypes):
            if v=='object':
                cat_cols.append(c)

        for col in cat_cols:
            df[col] = df[col].astype('category')
        df = df.dropna(subset=['num'])
        self.tr = df.drop('num', axis=1)
        self.te = df['num']
        
    def retrain(self):
        params = {
            'n_estimators':10,
            'num_leaves':13,
            'max_depth':4,
            'learning_rate':0.2,
            'random_state':42,
            'tree_method':'hist',
            'n_jobs':-1,
            'verbose': True,
            'evalmetrics':'logloss'
        }
        model = xgb.XGBClassifier(n_estimators=params['n_estimators'], learning_rate=params['learning_rate'], tree_method=params['tree_method'], n_jobs=params['n_jobs'], eval_metric='mlogloss'
                                , max_depth=params['max_depth'], enable_categorical=True)
        model.fit(self.tr,self.te)
        if os.path.exists('model.json'):
            cmd = 'sudo rm model.json'
            os.system(cmd)
        model.save_model("model.json")

    def prediction(self):
        pred = self.model.predict(self.tr)
        if pred[0]==0:
            self.res = 'Health'
        else:
            self.res = 'Potential Heart Disease'
        return self.res, pred[0]
    
        