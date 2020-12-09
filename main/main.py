from main import *

import requests
from flask_pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.myDatabase


@app.route('/get', methods=['GET'])
def gets():
    results = list(db.contents.find({}))
    return render_template('/home.html', results=results)


@app.route('/get/my', methods=['GET'])
def my_gets():
    userid_receive = request.user.userid
    my_result = list(db.contents.find({'userid':userid_receive}))
    return render_template('/mypage.html', my_result=my_result)