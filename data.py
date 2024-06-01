import pandas as pd
import os

FOLDER_PATH = "paths"


def get_data(filename):
    path = os.path.join(FOLDER_PATH, filename + ".csv")

    data = pd.read_csv(path)
    data = data.drop(data.index[0]) # delete first row

    X = data.iloc[:, 0].values
    Y = data.iloc[:, 1].values

    return X, Y
