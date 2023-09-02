from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hello_rec', methods=["POST"])
def hello_recommendation():
    try:
        if request.method == 'POST':
            req_json = request.get_data()
            rec_obj = json.loads(req_json)
            user_id = rec_obj["user_id"]
            return jsonify({"code": 0, "msg": "请求成功", "data": "hello " + user_id})
    except:
        return jsonify({"code": 2000, "msg": "error"})

if __name__ == '__main__':
    app.run()