from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
import json, sys, os
# from tools.Predict import Predict


app = Flask(__name__, template_folder='templates')
# predict = Predict()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print('username:{}, password:{}'.format(username, password), file=sys.stdout)
        global user, data
        try:
            file = open("data/json/" + username + ".json", 'r', encoding='utf-8')
            data = json.load(file)
            file.close()
        except FileNotFoundError:
            print("用户不存在", sys.stderr)
            print("data/json/" + username + ".json", sys.stderr)
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
        print("用户未登录", sys.stderr)
        return redirect(url_for('login'))
    else:
        return render_template('main.html', username=user)


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    return render_template('analysis.html')


@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    try:
        data
    except NameError:
        print("用户未登录", sys.stderr)
        return redirect(url_for('login'))
    else:
        return render_template('timeline.html', data=data)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    try:
        user
    except NameError:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
        # pick = predict.predict(user, 3)
        # print('recommend:', pick, file=sys.stdout)
        # return render_template('recommend.html', data=pick)


if __name__ == '__main__':
    app.run(debug=True)