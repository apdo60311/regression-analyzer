from flask import Flask, render_template
from scripts.model_evaluation import ModelEvaluation

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result')
def model_result():
    ModelEvaluation.plot_regression()
    return render_template('result.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)