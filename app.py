import sys

from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
import json, sys


app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            file = open("data/"+username+".json", 'r')
            data = json.load(file)
            file.close()
        except FileNotFoundError:
            print("用户不存在", sys.stderr)
        else:
            return render_template('main.html')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)