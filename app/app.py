from flask import Flask, render_template, request, redirect, url_for
from scripts.data_preprocessing import DataPreprocessing
from scripts.model_evaluation import ModelTrainig
from scripts.model_evaluation import ModelEvaluation
import numpy as np

app = Flask(__name__)


data_preprocessing = DataPreprocessing()
model_building: ModelTrainig = None
model_evaluation = None


@app.route('/',methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'GET':
            return render_template('index.html')
        elif request.method == 'POST':
            files = request.files.getlist('file')
            global model_building
            data_preprocessing.read_and_integrate_dataframes(files)
            model_building = ModelTrainig(data_preprocessing.df)
            return redirect('/loading')
    except:
      return redirect(url_for('error', message = 'File Not supported'))

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/error')
def error():
    message = request.args.get('message')
    return render_template('error.html', message = message)

@app.route('/earth')
def earth():
    try:
        country_c = data_preprocessing.df[['Country','Happiness Rank']].sort_values('Country').to_dict()
        return render_template('earth.html',country_c=country_c['Happiness Rank'])
    except:
        return redirect('/error')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/explore_data')
def explore_data():
    try:
        info = data_preprocessing.explore_dataframe()
        histograms = data_preprocessing.plot_histograms()
        heat_map = data_preprocessing.show_correlation_heatmap()
        corr_matrix = data_preprocessing.show_correlation_matrix()
        boxplot = data_preprocessing.plot_boxplot()

        return render_template('explore_data.html',info=info,heat_map=heat_map,corr_matrix=corr_matrix,boxplot=boxplot,histograms=histograms)
    except:
        return "<script> alert('Earth plot cannot be applied!') </script>"
        # return redirect('/error')
    
@app.route('/prepare_data', methods=['GET', 'POST'])
def prepare_data():
    try:
        if request.method == 'GET':
            df = data_preprocessing.df
            columns = df.select_dtypes(include=[np.number])
            return render_template('data_preparation.html', dataframe_name='DF', column_names=columns)
        else:
            target_variable = request.form['target_variable']
            features = request.form.getlist('features')
            remove_outliers = request.form['remove_outliers']
            remove_outlier_column = request.form['outlier_columns']
            remove_duplicates = request.form['remove-duplicates']
            remove_missing = request.form['remove-missing']
            normalize_data = request.form['normalize_data']
            
            if remove_outliers == 'yes':
                data_preprocessing.remove_outliers(remove_outlier_column)
            if remove_missing == 'yes':
                data_preprocessing.remove_missing_values()
            if remove_duplicates == 'yes':
                data_preprocessing.remove_duplicates()
            if normalize_data == 'yes':
                data_preprocessing.normalize_data()

            global model_building
            model_building.set_df(data_preprocessing.df)
            model_building.set_variables(features=features,dependent=target_variable)
            return redirect('/model_selection')
    except:
        return redirect('/error')
    
@app.route('/model_selection')
def model_selection_show():
    return render_template('model_selection.html')

@app.route('/model_selection/<string:model_name>')
def model_selection(model_name):
    try:
        if not model_name:
            return render_template('model_selection.html')
        else:
            global model_building    
            model_building.set_df(data_preprocessing.df)
            model_stats = model_building.build_model(model_name)
            global model_evaluation
            model_evaluation = ModelEvaluation(model_name=model_building.model_name,model_results=model_building.results,model_training=model_building)
            reg_plot = model_evaluation.plot_regression()
            learning_curve = model_evaluation.plot_learning_curve()
            return render_template('result.html',model_stats=model_stats,learning_curve=learning_curve, reg_plot = reg_plot)
    except:
        return redirect(url_for('error', message = 'prepare data first'))


@app.route('/result')
def model_result():
    try:
        reg_plot = model_evaluation.plot_regression()
        learning_curve = model_evaluation.plot_learning_curve()
        return render_template('result.html',model_stats=model_evaluation.model_results,learning_curve=learning_curve, reg_plot = reg_plot)
    except:
        return redirect(url_for('error', message='Prepare data first'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)