import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import  StratifiedKFold, train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, LabelBinarizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

def final_model(model, X_train, y_train):
    model = model
    model.fit(X_train, y_train)

    return model

def encode_labels(df):
    #Change values to disceret valuse via LabelEncoder
    #poisonous = 1
    le = LabelEncoder()
    df_2 = df.apply(le.fit_transform)

    X = df_2.loc[:, mushroom_df.columns != "class"]
    y = df_2.iloc[:, 0].as_matrix()

    #change label encoded df to onehotconcoding representation
    enc = OneHotEncoder()
    X_2 = enc.fit_transform(X)

    return X_2, y


if __name__ == '__main__':

    models = [("LR", LogisticRegression()), ("DTC", DecisionTreeClassifier()), ("SVC", SVC()), ("RFC", RandomForestClassifier())]

    mushroom_df = pickle.load(open("../data/mushroom_df.pkl", "rb"))

    X, y = encode_labels(mushroom_df)

    X_tr, X_validate, y_tr, y_validate = train_test_split(X, y, random_state = 6, stratify=y, test_size=.10)

    skf = StratifiedKFold(n_splits=5, random_state=6)
    scoring="recall"

    names = []
    results = []
    for name, model in models:
        SKFold = StratifiedKFold(n_splits=5, random_state=6)
        cv_results = cross_val_score(model, X_tr, y_tr, scoring=scoring, cv=SKFold)
        results.append(cv_results)
        names.append(name)
        msg = "{}: {} ({})".format(name, cv_results.mean(), cv_results.std())
        print(msg)

    model = final_model(LogisticRegression(), X, y)
