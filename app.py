from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
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
        data
    except NameError:
        return redirect(url_for('login'))
    else:
        return render_template('timeline.html', data=data)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    return render_template('recommend.html')


if __name__ == '__main__':
    app.run(debug=True)