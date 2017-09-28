import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

def import_data(filepath, df):
    with open(filepath, "r") as f:
        for i, line in enumerate(f):
            df.loc[i] = line.strip().split(" ")

    return df

def clean_df(df):
    df.loc[:, 'stalk_root'].replace("?", np.nan, inplace=True)
    df.dropna(inplace=True)

    pickle.dump(df, open("mushroom_df.pkl", "wb"))
    return df


if __name__ == '__main__':
    pd.set_option('display.max_columns', 23)
    mushroom_df =pd.DataFrame({"class":[], "cap_shape":[], "cap_surface":[],"cap_color":[],"bruises":[], "oder":[], "gill_attachment":[], "gill_spacing":[], "gill_size":[], "gill_color":[], "stalk_shape":[], "stalk_root":[], "stalk_surface_above_ring":[], "stalk_surface_below_ring":[], "stalk_color_above_ring":[], "stalk_color_below_ring":[], "veil_type":[], "veil_color":[], "ring_number":[], "ring_type":[], "spore_print_color":[], "population":[], "habitat":[]})

    #ordered df
    mushroom_df = mushroom_df[["class", "cap_shape", "cap_surface","cap_color","bruises", "oder", "gill_attachment", "gill_spacing", "gill_size", "gill_color", "stalk_shape", "stalk_root", "stalk_surface_above_ring", "stalk_surface_below_ring", "stalk_color_above_ring", "stalk_color_below_ring", "veil_type", "veil_color", "ring_number", "ring_type", "spore_print_color", "population", "habitat"]]

    import_data("../data/mushrooms/Dataset.data", mushroom_df)
    clean_df(mushroom_df)
