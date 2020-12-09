from main import *

# import requests
from flask_pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.myDatabase


@app.route('/get/my', methods=['GET'])
def gets():
    id_receive = session.get("id")
    results = list(db.contents.find({'writer_id':id_receive}))
    return render_template('/mypage.html', results=results)

@app.route('/get', methods=['GET'])
def maingets():
    mainresults = list(db.contents.find({}))
    return render_template('/home.html', mainresults=mainresults)