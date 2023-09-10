import pickle
import numpy as np
import pandas as pd
import argparse

# read argparse
parser = argparse.ArgumentParser()
parser.add_argument('user', type=str, help='eg:G20245555')
parser.add_argument('nums', type=int, help='eg:5')
args = parser.parse_args()

if __name__ == '__main__':
    # load data
    file = open('data/pkl/CF.pkl', 'rb')
    data = pickle.load(file)
    file.close()

    users = pd.read_csv('data/csv/users.csv', header=None)
    items = pd.read_csv('data/csv/items.csv', header=None)

    user = users[users.values == args.user].index.tolist()[0]
    pick = np.argpartition(data[user], -args.nums)[-args.nums:]

    file = open('data/tmp/' + args.user + '.txt', 'w')
    for x in pick:
        file.write(items.iloc[x].values[0])
        file.write('\n')
    file.close()