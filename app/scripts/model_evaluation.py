import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import plotly.express as px
from .model_training import ModelTrainig
from sklearn.model_selection import learning_curve


class ModelEvaluation:

    def __init__(self, model_name:str, model_results:list, model_training:ModelTrainig):
        self.model_name = model_name
        self.model_results = model_results
        self.model_training = model_training

    def plot_learning_curve(self):
        train_sizes, train_scores, test_scores = learning_curve(
            self.model_training.models[self.model_training.model_name],self.model_training.X,self.model_training.y, train_sizes=np.linspace(0.1, 1.0, 10), cv=5)

        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)

        test_mean = np.mean(test_scores, axis=1)
        test_std = np.std(test_scores, axis=1)

        trace_train = go.Scatter(x=train_sizes, y=train_mean, mode='lines', name='Training Score', line=dict(color='blue'))
        trace_test = go.Scatter(x=train_sizes, y=test_mean, mode='lines', name='Validation Score', line=dict(color='red'))

        fig = go.Figure([trace_train, trace_test])
        fig.add_trace(go.Scatter(x=train_sizes, y=train_mean - train_std,
                                mode='lines',
                                showlegend=False,
                                line=dict(width=0),
                                fill='tonexty',
                                fillcolor='rgba(128,128,128,0.2)'))

        fig.add_trace(go.Scatter(x=train_sizes, y=train_mean + train_std,
                                mode='lines',
                                showlegend=False,
                                line=dict(width=0),
                                fill='tonexty',
                                fillcolor='rgba(128,128,128,0.2)'))

        fig.add_trace(go.Scatter(x=train_sizes, y=test_mean - test_std,
                                mode='lines',
                                showlegend=False,
                                line=dict(width=0),
                                fill='tonexty',
                                fillcolor='rgba(128,128,128,0.2)')) 

        fig.add_trace(go.Scatter(x=train_sizes, y=test_mean + test_std,
                                mode='lines',
                                showlegend=False,
                                line=dict(width=0),
                                fill='tonexty',
                                fillcolor='rgba(128,128,128,0.2)'))  

        fig.update_layout(title='Learning Curve',
                        xaxis_title='Training Instances',
                        yaxis_title='Score',
                        hovermode='x',width=1250)
        return pio.to_html(fig=fig, full_html=False)

    

    def plot_regression(self):
        scatter_trace = go.Scatter(x=self.model_training.y_test, y=self.model_training.y_pred, mode='markers', marker=dict(color='blue'), name='Actual vs. Predicted')
        regression_trace = go.Scatter(x=self.model_training.y_test, y=self.model_training.y_test, mode='lines', line=dict(color='black', dash='dash'), name='Perfect Prediction')

        layout = go.Layout(title=self.model_name,
                        xaxis=dict(title="Actual Happiness Score"),
                        yaxis=dict(title="Predicted Happiness Score"),
                        width=1250)

        fig = go.Figure(data=[scatter_trace, regression_trace], layout=layout)
        return pio.to_html(fig=fig, full_html=False)
