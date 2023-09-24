from tools.DSSM import DSSM
import numpy as np
import pandas as pd
import paddle, json, random


class Predict:
    def __init__(self):
        self.users = pd.read_csv('data/csv/users.csv')
        self.items = pd.read_csv('data/csv/items.csv')
        self.dssm = DSSM(len(self.users), len(self.items))
        self.dssm.set_state_dict(paddle.load('data/net/model.pdparams'))

    def predict(self, username, nums):
        user = self.users[self.users.values == username].index.tolist()[0]
        mark = self.dssm(paddle.to_tensor([[user, item] for item in range(len(self.items))], dtype='int32'))
        mark = mark.numpy()

        read = np.zeros(len(self.items))
        try:
            file = open('data/json/'+username+'.json', 'r')
            data = json.load(file)
            file.close()
            for x in data:
                idx = self.items[self.items.values == x['name']].index.tolist()[0]
                read[idx] = -1
        finally:
            mark = mark - read
        pick = mark.argsort()[-nums*3:]
        pick = random.sample(list(pick), nums)
        name = self.items.iloc[pick]
        return name


