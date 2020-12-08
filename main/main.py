from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from flask_pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.mydatabase


@app.route('/get', methods=['GET'])
def gets():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.contents.find({}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return render_template('/home.html', result=result)


@app.route('/get/my', methods=['GET'])
def my_gets():
    userid_receive = request.user.userid
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    my_result = list(db.contents.find({'userid':userid_receive}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return render_template('/mypage.html', my_result=my_result)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)