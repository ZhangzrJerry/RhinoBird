import pickle
import numpy as np
import pandas as pd


def predict(user, nums=5):
    file = open('data/pkl/CF.pkl', 'rb')
    data = pickle.load(file)
    file.close()

    users = pd.read_csv('data/csv/users.csv', header=None)
    items = pd.read_csv('data/csv/items.csv', header=None)

    user = users[users.values == user].index.tolist()[0]
    pick = np.argpartition(data[user], -nums)[-nums:]

    return [items.iloc[x].values[0] for x in pick]