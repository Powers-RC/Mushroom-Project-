from flask import render_template, request, redirect, flash, url_for, session
from _init_ import app
from forms import feature_string
import sys
import pickle
import pandas as pd


@app.route('/')
@app.route('/home')
def home():
    form = feature_string()
    return render_template('home.html', methods=['GET, POST'], form=form)
    # form = feature_string()
    # if request.method == "POST":
    #     return render_template('home.html', methods=['GET, POST'], form=form)
    #     # redirect(url_for('/home_post'))
    #     #check validators
    # else:
    #     return render_template('home.html', methods=['GET, POST'], form=form)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/visualizations')
def visualizations():
    return render_template('visualizations.html')

@app.route('/data_source')
def data_source():
    return render_template('data_source.html')

@app.route('/prediction')
def prediction():
    # return ("Testing...testing...{} ").format(request.args.get('result'))
    return render_template('prediction.html', result=request.args.get('result'))

@app.route('/submission', methods = ['GET','POST'])
# @app.route('/submission/<string:attr_list>', methods = ['GET', 'POST'])
def submission(attr_list=None):
    form = feature_string(request.form)
    error = None

    if request.method == 'POST' and form.validate_on_submit():
        attr_list = request.form['input_attr'].strip()
        attr_list = [i for i in list(attr_list) if i != ',']

        len_check = len(attr_list)

        if len_check != 5:
            error = "Not all parameters were selected before submission"
            return render_template('home.html', error=error, form=form, methods=["GET", "POST"])

        else:
            flash("You successfully submitted your mushroom characteristics")

            model = pickle.load(open('../mushroom_classification/src/mushroom_model.pkl','rb'))
            encoding = pickle.load(open('../mushroom_classification/src/mushroom_le.pkl','rb'))

            data_dic = {"stalk_shape": [], "odor": [], "gill_size":[], "spore_print_color":[], "habitat":[]}
            # ["stalk_shape","oder","gill_size","spore_print_color","habitat"]
            data_dic["stalk_shape"] = attr_list[0]
            data_dic["odor"] = attr_list[1]
            data_dic["gill_size"] = attr_list[2]
            data_dic["spore_print_color"] = attr_list[3]
            data_dic["habitat"] = attr_list[4]


            df = pd.DataFrame(data_dic, index=[0])
            # return ("Testing......{}").format(df)
            transformed_df = df.apply(lambda x: encoding[x.name].transform(x))
            len_check = len(transformed_df.as_matrix()[0])
            # return ("Testing......{}").format(transformed_df.as_matrix()[0])
            results = int(model.predict(transformed_df.as_matrix())[0])
            # return ("Testing......{}").format(len_check)
            return redirect(url_for('prediction', result=results))
    else:
        error = "Please agree to our terms and select your parameters again!"
        return render_template('home.html', error=error, form=form, methods=["GET", "POST"])

        # ("Testing......{}").format(model.predict(transformed_df.as_matrix()))

        # 1:posionous 0:edible

        # You will likely have to transform this df back to a list of strings to call prediction.
        # prediction = model.predict(transformed_df)
        #
        #
        # # call function with reference to html based on results
        # '''If mushroom is poisonous'''
        # return render_template('prediction.html')
        #
        # '''If mushroom is not poisonous'''
        # return render_template('not_poisonous.hml')

'''you could also use a single html script and loading symbol and return an image based on result'''
