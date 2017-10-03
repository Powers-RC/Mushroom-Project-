from flask import render_template, request, redirect, flash
from _init_ import app
from forms import feature_string

@app.route('/')
@app.route('/home')
def home():
    featrue_lst = []
    form = feature_string()
    if request.method == "POST":
        redirect(url_for('/home_post'))
    else:
        return render_template('home.html', methods=['GET, POST'], form=form)

@app.route('/home_post')
def prediction_page():
    data = request.form
    return render_template('prediction.html', methods=['GET, POST'], data=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/visualizations')
def visualizations():
    return render_template('visualizations.html')

@app.route('/data_source')
def data_source():
    return render_template('data_source.html')
