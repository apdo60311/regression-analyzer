# Regression Analyser

Regression analyser is a Flask web application that allows users to perform regression analysis on their data. It provides a user-friendly interface for uploading data files, selecting independent and dependent variables, and running various regression models. The application generates detailed reports with visualizations, model summaries, and plots to help users understand the relationships between variables.

## Features

1. Read datframe files as csv, xlsx, and more
2. Explore data and perform some data preprocessing tasks
3. Building simple/multiple regression model
4. Plot model's result
5. Also contains Earth visualization (in case dataframes with country column)

## Folder Structure

* [app/](.\happiness-regression\app)
  * [scripts/](.\happiness-regression\app\scripts)
  * [static/](.\happiness-regression\app\static)
  * [templates/](.\happiness-regression\app\templates)
  * [app.py](.\happiness-regression\app\app.py)
* [data/](.\happiness-regression\data)
  * [2015.csv](.\happiness-regression\data\2015.csv)
  * [2016.csv](.\happiness-regression\data\2016.csv)
  * [2017.csv](.\happiness-regression\data\2017.csv)
  * [2018.csv](.\happiness-regression\data\2018.csv)
* [documentation/](.\happiness-regression\documentation)
* [notebooks/](.\happiness-regression\notebooks)
  * [regression_model.ipynb](.\happiness-regression\notebooks\regression_model.ipynb)

* `app/` folder contains web application files.
  * `scripts/` folder contains all scripts that used in the app.
  * `static/` folder contains images, css, and javascript.
  * `templates/` folder contains all html pages
  * `app.py` is the main script that run the web application

* `data/` containes happiness dataframe for testing the application

* `notebooks/` containes jupyter notebooks

### Installation

1. Clone the repository: `git clone https://github.com/apdo60311/regression-analyzer`
2. Navigate to the project directory: `cd regression-analyzer`
3. Create a virtual environment: `python -m venv env`
4. Activate the virtual environment:
   * On Windows: `env\Scripts\activate`
   * On Unix or Linux: `source env/bin/activate`
5. Install the required packages: `pip install -r requirements.txt`

### Usage

1. Run the Flask application: `flask run` or `python app.py`
2. Open your web browser and visit `http://localhost:5000`

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b my-feature-branch`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-feature-branch`
5. Submit a pull request

### License

This project is licensed under the [MIT License](LICENSE).

### Contact

If you have any questions or suggestions, feel free to reach out to [apdo60311@gmail.com](apdo60311@gmail.com).
