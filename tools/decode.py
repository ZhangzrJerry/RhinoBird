import pandas as pd
from tqdm import tqdm
import json
from datetime import datetime, date, time


if __name__ == '__main__':
    df = pd.read_csv('../data/csv/读者借阅数据.csv', encoding='gbk')
    users = pd.read_csv('../data/csv/users.csv', header=None)

    for user in tqdm(users.values):
        data = []
        for item in df[(df['借书证号'] == user[0])].values:
            dura = datetime(
                int(item[5][0:4]),
                int(item[5][5:7]),
                int(item[5][8:10])) \
            - datetime(
                int(item[4][0:4]),
                int(item[4][5:7]),
                int(item[4][8:10])
            )
            data.append(
                {
                    "name": item[7],
                    "borrow": item[4],
                    "return": item[5],
                    "dura": dura.days
                }
            )
        file = open('../data/json' + user[0] + '.json', 'w', encoding='UTF-8')
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.close()