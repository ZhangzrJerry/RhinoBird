from flask import Flask, render_template

server = Flask(__name__, template_folder='templates')

@server.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    server.run(debug=True)