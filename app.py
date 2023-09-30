from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
import json, sys, os
from tools.calculate_duration import calculate_duration
from tools.analysis import analysis_data
from tools.Predict import Predict


app = Flask(__name__, template_folder='templates')
predict = Predict()


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
    try:
        data
        average_pages_per_day, average_rating_count, average_rating, most_read_type_data, most_read_count, total_borrow_count, \
            max_borrow_month, max_borrow_count, max_return_month, max_return_count, longest_reading_book, longest_reading_time, \
            characteristics, most_common_author, most_common_author_count = analysis_data(data)
        average_pages_per_day = average_pages_per_day.__round__(1)
        average_rating_count = average_rating_count.__round__(1)
        average_rating = average_rating.__round__(1)
        characteristics_string = ""
        for item in characteristics:
            characteristics_string += item + " "
    except NameError:
        print("用户未登录", sys.stderr)
        return redirect(url_for('login'))
    return render_template('analysis.html', data=data, username=user, average_pages_per_day=average_pages_per_day,
                           average_rating_count=average_rating_count, average_rating=average_rating,
                           most_read_type_data=most_read_type_data, most_read_count=most_read_count,
                           total_borrow_count=total_borrow_count, max_borrow_month=max_borrow_month,
                           max_borrow_count=max_borrow_count, max_return_month=max_return_month,
                           max_return_count=max_return_count, longest_reading_book=longest_reading_book,
                           longest_reading_time=longest_reading_time, characteristics=characteristics_string,
                           most_common_author=most_common_author, most_common_author_count=most_common_author_count)


@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    try:
        data
        dura_sum = calculate_duration(data)
    except NameError:
        print("用户未登录", sys.stderr)
        return redirect(url_for('login'))
    else:
        return render_template('timeline.html', data=data,username=user, dura=dura_sum)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    try:
        user
    except NameError:
        return redirect(url_for('login'))
    else:
        pick = predict.predict(user, 3)
        print('recommend:', pick, file=sys.stdout)
        return render_template('recommend.html', data=pick)


if __name__ == '__main__':
    app.run(debug=True)