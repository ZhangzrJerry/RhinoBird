from flask import Flask, render_template

server = Flask(__name__)

@server.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('html/login.html')

if __name__ == '__main__':
    server.run(debug=True)