import numpy as np
import plotly.graph_objs as go
import os


class ModelEvaluation:
    def plot_regression():
        # Generate dummy data
        np.random.seed(0)
        X = np.random.rand(100) * 10  # Independent variable
        y = 2 * X + np.random.randn(100) * 2  # Dependent variable with noise

        # Perform linear regression
        coefficients = np.polyfit(X, y, 1)  # Fit a first-degree polynomial (linear regression)
        line_of_best_fit = np.polyval(coefficients, X)  # Generate line of best fit

        # Create scatter plot trace for data points
        scatter_trace = go.Scatter(x=X, y=y, mode='markers', name='Data Points')

        # Create line plot trace for line of best fit
        line_trace = go.Scatter(x=X, y=line_of_best_fit, mode='lines', name='Line of Best Fit')

        # Define layout
        layout = go.Layout(title='Linear Regression on Dummy Data',
                        xaxis=dict(title='X'),
                        yaxis=dict(title='y'),
                        template='plotly_dark')  # Dark theme

        # Create figure
        fig = go.Figure(data=[scatter_trace, line_trace], layout=layout)

        fig.write_html(os.path.join('static', 'plots', 'plot.html'))