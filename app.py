from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session
import json, sys, os


app = Flask(__name__, template_folder='templates')
secret_key = os.environ.get("SECRET_KEY")


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/index', methods=['GET', 'POST'])
def main():
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
            session['user'] = username
            session['data'] = data
            return render_template('home.html')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)