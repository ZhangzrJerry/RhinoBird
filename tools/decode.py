import pandas as pd
from tqdm import tqdm
import json
from datetime import datetime, date, time


if __name__ == '__main__':
    df = pd.read_csv('../data/csv/读者借阅数据.csv', encoding='gbk')
    users = pd.read_csv('../data/csv/users.csv', header=None)
    types = {
        "A": "马克思主义、列宁主义、毛泽东思想、邓小平理论",
        "B": "哲学、宗教",
        "C": "社会科学总论",
        "D": "政治、法律",
        "E": "军事",
        "F": "经济",
        "G": "文化、科学、教育、体育",
        "H": "语言、文字",
        "I": "文学",
        "J": "艺术",
        "K": "历史、地理",
        "N": "自然科学总论",
        "O": "数理科学和化学",
        "P": "天文学、地球科学",
        "Q": "生物科学",
        "R": "医药、卫生",
        "S": "农业科学",
        "T": "工业技术",
        "U": "交通运输",
        "V": "航空、航天",
        "X": "环境科学、安全科学",
        "Z": "综合性图书"
    }

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
                    "type": types[item[6][0]],
                    "dura": dura.days
                }
            )
        file = open('../data/json/' + user[0] + '.json', 'w', encoding='UTF-8')
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.close()