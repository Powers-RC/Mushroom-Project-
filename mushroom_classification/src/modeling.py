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
from sklearn.feature_selection import RFE, RFECV
from collections import defaultdict

def final_model(model, X_train, y_train):
    model = model
    model.fit(X_train, y_train)
    pickle.dump(model, open('mushroom_model.pkl', 'wb'))

    return model

def encode_labels(df):
    """Get Label Encodings For Each On Of The Features...some error"""
    #Change values to disceret value via LabelEncoder
    #poisonous = 1
    #label ecoding for all features
    # le = LabelEncoder()
    # df_2 = df.apply(le.fit_transform)
    #
    # X = df_2.loc[:, mushroom_df.columns != "class"]
    # y = df_2.iloc[:, 0].as_matrix()

    #label encoding for relevant features

    d = defaultdict(LabelEncoder)
    attr_df = df.loc[:, ["classes", "stalk_shape", "odor", "gill_size", "spore_print_color", "habitat"]]
    # class_df = df.iloc[:, 0]

    le_df = attr_df.apply(lambda x: d[x.name].fit_transform(x))
    pickle.dump(le_df, open('label_encoded_df.pkl', 'wb'))
    pickle.dump(d, open('mushroom_le.pkl', 'wb'))

    # data_dic = {"stalk_shape": ["e"], "oder": ["a"], "gill_size":["b"], "spore_print_color":["k"], "habitat":["g"]}
    # test_df = pd.DataFrame(data_dic)
    #
    # print(test_df.head())
    # transform = test_df.apply(lambda x: d[x.name].transform(x))
    # print(transform)
    #
    # for k,v in d.items():
    #     print("{}: {}".format(k, v.classes_))
    #
    return(d,le_df)








    # pickle.dump(label_encoder, open('label_encoder.pkl', 'wb'))
    #change label encoded df to onehotconcoding representation
    # enc = OneHotEncoder()
    # X_2 = enc.fit_transform(X)

    # return X_2, y
    # return X, y
    # return le

def feature_selection_rfecv(model, X_tr, X_validate, y_tr, y_validate):
    # for name, model in models:
    m = model
    rfecvm = RFECV(m, cv=5, scoring='recall')
    fm = rfecvm.fit(X_tr,y_tr)
    print("Number of features: {}".format(fm.n_features_))
    print("Selected features: {}".format(fm.support_))
    print("Feature rankings: {}".format(fm.ranking_))
    print("Estimated score on the reduced set: {}".format(fm.score(X_validate, y_validate)))

    plt.figure()
    plt.xlabel("Number of Features Selected")
    plt.ylabel("Cross Validation Score (Recall)")
    plt.title("Recursive Feature Elimination")
    plt.plot(range(1, len(fm.grid_scores_)+1), fm.grid_scores_)
    # plt.show()
    plt.savefig("../../images/RFECVGraph.png")

def feature_selection_rfe(model, X_tr, X_validate, y_tr, y_validate):
    # for name, model in models:
    m = model
    # rfem = RFE(m, 6)
    # fm = rfem.fit(X_tr,y_tr)
    fm = m.fit(X_tr, y_tr)
    # print("Number of features: {}".format(fm.n_features_))
    # print("Selected features: {}".format(fm.support_))
    # print("Feature rankings: {}".format(fm.ranking_))
    # print("Estimated score on the reduced set: {}".format(fm.score(X_validate, y_validate)))
    # print(impt_features(fm.support_, X_tr.columns))

    importances = fm.feature_importances_
    indicies = np.argsort(importances)[::-1]
    std = np.std([tree.feature_importances_ for tree in fm.estimators_], axis=0)

    plt.figure()
    plt.bar(range(X_tr.shape[1]), importances[indicies], color='r', align='center', yerr=std[indicies])
    plt.xticks(range(X_tr.shape[1]), indicies)
    plt.title("Feature Importances")
    plt.ylabel("Gini Index")
    plt.xlabel("Feature Indicies")
    plt.xlim([-1, X_tr.shape[1]])
    plt.plot()
    # plt.show()
    plt.savefig("../../images/FeatureImportanceGraph.png")

def impt_features(bool_lst, columns):
    features = []
    for i, val in enumerate(bool_lst):
        if val == True:
            features.append(columns[i])
    return features

def dt_feature_impt(model, X_tr, X_validate, y_tr, y_validate):
    m = model
    m.fit(X_tr, y_tr)
    impt_lst = m.feature_importances_
    bool_impt_lst = [True if val > 0.02 else False for val in impt_lst]
    impt_lst = [ val for val in impt_lst if val > 0.02 ]
    col_names = impt_features(bool_impt_lst, X_tr.columns)
    print(list(zip(col_names, impt_lst)))

if __name__ == '__main__':

    init_df = pd.read_csv('../data/mushrooms/Dataset.data', delim_whitespace=True, header=None, names=['classes', 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor', 'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color', 'stalk-shape', 'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring', 'stalk-color-above-ring', 'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number', 'ring-type', 'spore-print-color', 'population', 'habitat'])

    init_df['stalk-root'].replace('?', init_df['stalk-root'].max(), inplace=True)


    init_df.rename(columns={"cap-shape": "cap_shape", "cap-surface":"cap_surface", "cap-color":"cap_color", "gill-attachment":"gill_attachment", "gill-spacing":"gill_spacing", "gill-size":"gill_size", "gill-color":"gill_color", "stalk-shape":"stalk_shape", "stalk-root":"stalk_root", "stalk-surface-above-ring":"stalk_surface_above_ring","stalk-surface-below-ring":"stalk_surface_below_ring","stalk-color-above-ring":"stalk_color_above_ring", "stalk-color-below-ring":"stalk_color_below_ring", "veil-type":"veil_type", "veil-color":"veil_color", "ring-number":"ring_number", "ring-type":"ring_type", "spore-print-color":"spore_print_color"}, inplace=True)


    refined_mush_df = init_df.loc[:, ["classes", "odor", "gill_size", "stalk_shape", "spore_print_color", "habitat"]]

    models = [("LR", LogisticRegression(random_state=6)), ("DTC", DecisionTreeClassifier(random_state=6)), ("SVC", SVC(kernel="linear", random_state=6)), ("RFC", RandomForestClassifier(n_estimators=1000, random_state=6,  max_features=None))]

    # mushroom_df = pickle.load(open("../data/mushroom_df.pkl", "rb"))
    # mushroom_df = pd.read_pickle(str("mushroom_df.pkl"))


    d,le_df = encode_labels(refined_mush_df)
    # encode_labels(refined_mush_df)

    le_df = pickle.load(open('label_encoded_df.pkl', 'rb'))
    X = le_df.loc[:, ["stalk_shape", "odor", "gill_size", "spore_print_color", "habitat"]]
    y = le_df.loc[:,"classes"]
    X_train, X_holdout, y_train, y_holdout = train_test_split(X,y, random_state=6, stratify=y, test_size=.10)

    final_model(DecisionTreeClassifier(random_state=6), X_train, y_train)


    # X_tr, X_validate, y_tr, y_validate = train_test_split(X_train, y_train, random_state = 6, stratify=y_train, test_size=.10)

    #feature importance
    # dt_feature_impt(models[3][1], X_tr, X_validate, y_tr, y_validate)
    '''
    [('odor', 0.065296723725987826), ('gill_size', 0.16111470082275664), ('stalk_shape', 0.022105356396894104), ('spore_print_color', 0.68311560998062382), ('habitat', 0.028052161700809257)]
    '''


    #recursive feature elimination
    # feature_selection_rfecv(models[3][1], X_tr, X_validate, y_tr, y_validate)


    # skf = StratifiedKFold(n_splits=5, random_state=6)
    # scoring="recall"
    #
    # names = []
    # results = []
    # for name, model in models:
    #     SKFold = StratifiedKFold(n_splits=5, random_state=6)
    #     cv_results = cross_val_score(model, X_tr, y_tr, scoring=scoring, cv=SKFold)
    #     results.append(cv_results)
    #     names.append(name)
    #     msg = "{}: {} ({})".format(name, cv_results.mean(), cv_results.std())
    #     print(msg)
    #
    # model = final_model(models[1][1], X, y )

    #save this models, make sure data is label and hot encoded correctly
