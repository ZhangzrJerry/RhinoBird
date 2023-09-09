from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
from collections import defaultdict
import json
import json, sys, os


app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        global user, data
        try:
            file = open("data/"+username+".json", 'r')
            data = json.load(file)
            file.close()
        except FileNotFoundError:
            print("用户不存在", sys.stderr)
        else:
            user = username
            return redirect(url_for('main'))
    return render_template('login.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        if 'timeline' in request.form.to_dict().keys():
            return redirect(url_for('timeline'))
        if 'analysis' in request.form.to_dict().keys():
            return redirect(url_for('analysis'))
        if 'recommend' in request.form.to_dict().keys():
            return redirect(url_for('recommend'))
    try:
        user
    except NameError:
        return redirect(url_for('login'))
    else:
        return render_template('main.html', username=user)


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    return render_template('analysis.html')


@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    try:
        data = [
    {
        "date": "2023-06-02",
        "name": "百科全书",
        "dura": 300,
        "type": "百科"
    },
    {
        "date": "2023-06-08",
        "name": "孙子兵法",
        "dura": 60,
        "type": "军事"
    },
    {
        "date": "2023-06-12",
        "name": "梦里花落知多少",
        "dura": 180,
        "type": "小说"
    },
    {
        "date": "2023-06-18",
        "name": "论语",
        "dura": 90,
        "type": "哲学"
    },
    {
        "date": "2023-06-22",
        "name": "水浒传",
        "dura": 240,
        "type": "小说"
    },
    {
        "date": "2023-06-28",
        "name": "麦田里的守望者",
        "dura": 150,
        "type": "小说"
    },
    {
        "date": "2023-07-04",
        "name": "动物农场",
        "dura": 120,
        "type": "小说"
    },
    {
        "date": "2023-07-10",
        "name": "傲慢与偏见",
        "dura": 210,
        "type": "小说"
    },
    {
        "date": "2023-07-16",
        "name": "飘",
        "dura": 300,
        "type": "小说"
    },
    {
        "date": "2023-08-03",
        "name": "老人与海",
        "dura": 90,
        "type": "小说"
    },
    {
        "date": "2023-08-09",
        "name": "天龙八部",
        "dura": 300,
        "type": "小说"
    },
    {
        "date": "2023-08-15",
        "name": "金瓶梅",
        "dura": 240,
        "type": "小说"
    },
    {
        "date": "2023-08-21",
        "name": "茶花女",
        "dura": 180,
        "type": "小说"
    },
    {
        "date": "2023-08-27",
        "name": "西游记",
        "dura": 270,
        "type": "小说"
    }
]
        
        # timeline需要提供的数据：月份，本月总计时长，阅读最久的一本书，读的最多的一种类型
        monthly_data = []
        monthly_reading = defaultdict(lambda: {"total_duration": 0, "max_duration": 0, "max_duration_book": "", "type_counts": {},"max_type": "", "max_type_duration": 0})
        for each_book in data:
            date = each_book["date"]
            month = int(date.split("-")[1].lstrip("0"))
            duration = each_book["dura"]
            book_name = each_book["name"]
            book_type = each_book["type"]
            # 计算特定月份总时长
            monthly_reading[month]["total_duration"] += duration
            # 超级抽象的排序
            if duration > monthly_reading[month]["max_duration"]:
                monthly_reading[month]["max_duration"] = duration
                monthly_reading[month]["max_duration_book"] = book_name
            if book_type not in monthly_reading[month]["type_counts"]:
                monthly_reading[month]["type_counts"][book_type] = 0
            # 处理type
            monthly_reading[month]["type_counts"][book_type] += duration
            max_type = max(monthly_reading[month]["type_counts"], key=lambda x: monthly_reading[month]["type_counts"][x])
            monthly_reading[month]["max_type"] = max_type
            monthly_reading[month]["max_type_duration"] = monthly_reading[month]["type_counts"][max_type]
            # 将monthly_rading字典转换为JSON格式
            # 这一块逻辑有点混乱，主要是我想把month塞进json里面
        for month, info in monthly_reading.items():
            max_type = max(info["type_counts"], key=lambda x: info["type_counts"][x])
            max_type_duration = info["type_counts"][max_type]
            monthly_data.append({
                "month": month,
                "total_duration": info["total_duration"],
                "max_duration": info["max_duration"],
                "max_duration_book": info["max_duration_book"],
                "max_type": max_type,
                "max_type_duration": max_type_duration
            })
        monthly_data_json = json.dumps(monthly_data, ensure_ascii=False, indent=4)
        print(monthly_data_json)
        return render_template('timeline.html', monthly_data_json=monthly_data_json)
        
    except NameError:
        return redirect(url_for('login'))
    else:
        return render_template('timeline.html', monthly_data_json=monthly_data_json)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    return render_template('recommend.html')


if __name__ == '__main__':
    app.run(debug=True)