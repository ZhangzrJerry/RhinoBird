from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)