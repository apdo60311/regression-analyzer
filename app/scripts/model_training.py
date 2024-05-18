from sklearn.linear_model import(
    HuberRegressor,
    LinearRegression,
    RANSACRegressor,
    TheilSenRegressor,
    ElasticNet,
    SGDRegressor,
    BayesianRidge,
    Ridge,
    LogisticRegression,
    ARDRegression,
    QuantileRegressor
    )
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import pandas as pd

class ModelTrainig:
    models = {
    'SVR': SVR(degree=7, kernel='rbf', C=10, gamma=0.1),
    'LinearRegression':LinearRegression(),
    'Huber': HuberRegressor(alpha=0.0001, max_iter=10000),
    'RANSAC':RANSACRegressor(),
    'BayesianRidge': BayesianRidge(alpha_1=0.1, lambda_1=0.1),
    'TheilSen': TheilSenRegressor(random_state=0),
    'Ridge': Ridge(alpha=1.0)
    }

    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.X = None
        self.y = None

    def set_df(self, df):
        self.df = df

    def set_variables(self, features, dependent:str):
        self.X = self.df[features]
        self.y = self.df[dependent]
        

    def build_model(self,model_name:str):
        self.model_name = model_name
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)
        
        self.fitted_model = self.models[model_name].fit(self.X_train, self.y_train)
        self.y_pred = self.models[model_name].predict(self.X_test)

        mae = mean_absolute_error(self.y_test, self.y_pred)
        mse = mean_squared_error(self.y_test, self.y_pred)
        r2e = np.sqrt(mean_squared_error(self.y_test, self.y_pred))
        r2 = r2_score(self.y_test, self.y_pred)

        coeff = dict(zip(self.df.columns, self.fitted_model.coef_))

        self.results = [r2,mae,mse,r2e,coeff]
        self.results_labels = ['R-squared','Mean Absolute Error','Mean Squared Error','Root Square Error','Coefficients']
        self.results = dict(zip(self.results_labels, self.results))
        return self.results
    