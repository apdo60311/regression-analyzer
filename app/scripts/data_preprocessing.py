import math
import pandas as pd
import plotly.io as pio
import plotly.graph_objs as go
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler

# import plotly.graph_objects as go

class DataPreprocessing:
    def __init__(self):
        self.df:pd.DataFrame = None
    def read_dataframe(self,file) -> pd.DataFrame:
        """Reads a dataframe from a file storage.

        Args:
            file (FileStorage): The file storage to read the dataframe from.

        Returns:
            pd.DataFrame: The dataframe read from the file storage object.
        """

        file_extension = file.filename.split(".")[-1].lower()

        if file_extension == "csv":
            self.df = pd.read_csv(file)
        elif file_extension == "xlsx":
            self.df = pd.read_excel(file)
        elif file_extension == "json":
            self.df = pd.read_json(file)
        elif file_extension == "parquet":
            self.df = pd.read_parquet(file)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

        return self.df


    def read_and_integrate_dataframes(self,files:list):
        """
        Reads multiple dataframe files from list of paths and combine them into one dataframe
                
        Args:
            paths (list): A list of paths of dataframe files.
        
        Returns:
            None
        """
        if len(files) == 0:
            self.df = self.read_dataframe(files[0])
        else:
            dfs = []
            for file in files:
                dfs.append(self.read_dataframe(file))
            self.df = pd.concat(dfs)
            
    def check_country_col(self):
        for col in self.df.columns:
            if 'country' in col.lower():
                self.country_col = col
                return col
        return None
    def create_earth_plot(self , column_name:str)->go.Figure:
        """
        Generates a choropleth map visualization.
        
        Args:
            self (object): The instance of the class containing the DataFrame.
        
        Returns:
            go.Figure: A Plotly figure object representing the choropleth map.
        """
        country_col_name = self.check_country_col()

        earth = dict(type = 'choropleth', 
           locations = self.df['Country'],
           locationmode = 'country names',
           z = self.df[country_col_name], 
           text = self.df[column_name],
          colorscale = 'Viridis', reversescale = False,
          hovertemplate='hh')
        layout = dict(title = '{} Across the World'.format(column_name.capitalize()), 
                    geo = dict(showframe = False, 
                            projection = {'type': 'kavrayskiy7'}))
        figure = go.Figure(data = [earth], layout=layout)
        return pio.to_html(fig=figure)
    def explore_dataframe(self):
        null_count = self.df.isnull().sum().to_dict()
        duplicates_count = self.df.duplicated().sum()
        df_description = self.df.describe().to_dict()
        df_columns = self.df.columns.tolist()
        return {
        'null_count': null_count,
        'duplicates_count':duplicates_count,
        'description': df_description,
        'columns': df_columns
        }  
      

    def plot_histograms(self):
        num_cols = len(self.df.columns)
        rows = (num_cols + 1) // 2
        cols = 2

        fig = make_subplots(rows=rows, cols=cols)

        for i, col in enumerate(self.df.columns, 1):
            row_idx = (i - 1) // cols
            col_idx = (i - 1) % cols
            fig.add_trace(go.Histogram(x=self.df[col], name=col), row=row_idx+1, col=col_idx+1)

        fig.update_layout(title='Histograms of Columns',
                        barmode='overlay',
                        width=1250, height=1350,
                        xaxis=dict(title='Values'),
                        yaxis=dict(title='Density'),
                        template='plotly_dark')
        return pio.to_html(fig=fig, full_html=False)
    

    def plot_boxplot(self):
        traces = []

        for column in self.df.columns:
            trace = go.Box(y=self.df[column], name=column)
            traces.append(trace)

        layout = go.Layout(title='Boxplot',
                        yaxis=dict(title='Values'))

        fig = go.Figure(data=traces, layout=layout)
        fig.update_layout(width=1250,height=800)

        # return fig.to_html(full_html=False)
        return pio.to_html(fig=fig, full_html=False)
    

    
    def remove_outliers(self, column:str):
        """
        Removes outliers from the specified column in the DataFrame using IQR method
        
        Args:
            column (str): The column's name to remove outliers.
        
        Returns:
            None    
        """
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df_filtered = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]
        
        self.df = df_filtered

    def remove_missing_values(self):
        self.df = self.df.dropna()

    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()

    def normalize_data(self):
        """
        Normalizes the numerical columns of the DataFrame using Min-Max scaling.

        Args:
            None

        Returns:
            None
        """

        numerical_cols = self.df.select_dtypes(include=['number']).columns

        scaler = MinMaxScaler()

        self.df[numerical_cols] = scaler.fit_transform(self.df[numerical_cols])



    def show_correlation_matrix(self):
        dimensions = []
        for col in self.df.columns:
            dimensions.append(dict(label=col, values=self.df[col]))
        fig = go.Figure(data=go.Splom(
                dimensions=dimensions,
                showupperhalf=True, 
                marker=dict(color='black', 
                            # showscale=True, 
                            size=3,
                            line=dict(width=0.5, color='rgb(230,230,230)'))
                ))

        fig.update_layout(title='Relation between features', width=1250,height=1400,font=dict(size=8))
        return pio.to_html(fig=fig, full_html=False)

    def show_correlation_heatmap(self):
        corr_matrix = self.df.corr(numeric_only=True)

        heatmap_trace = go.Heatmap(z=corr_matrix.values,
                                x=corr_matrix.columns,
                                y=corr_matrix.columns,
                                colorscale='RdBu',
                                colorbar=dict(title='Correlation'),
                                hoverinfo='text')

        layout = go.Layout(title='Correlation Heatmap',
                        xaxis=dict(title='Features'),
                        yaxis=dict(title='Features'))
        annotations = []
        for i, row in enumerate(corr_matrix.values):
            for j, value in enumerate(row):
                annotations.append(
                    dict(
                        x=corr_matrix.columns[j],
                        y=corr_matrix.columns[i],
                        text=str(round(value, 2)),
                        font=dict(color='white' if abs(value) > 0.5 else 'black'),  
                        showarrow=False
                    )
                )

        layout.update(annotations=annotations, width=1250,height=800)

        fig = go.Figure(data=[heatmap_trace], layout=layout)

        # return fig.to_html(full_html=False)
        return pio.to_html(fig=fig, full_html=False)
