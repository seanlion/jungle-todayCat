<<<<<<< HEAD
from flask import Flask,render_template
=======
from flask import Flask,render_template,jsonify,request,session,redirect,url_for
>>>>>>> eb36522c1db52a6df6901e57c48892c0cbce30e6
from flask_pymongo import PyMongo
from datetime import datetime,timezone,timedelta
import os,re
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('signup.html')

BOARD_IMAGE_PATH = "/Users/seung/Desktop/backend/todaycat/images"
ALLOWED_EXTENSIONS = set(['png','pdf','jpg', 'jpeg','gif'])
# 이미지 경로에 쉽게 접근하기 위해 환경 변수 생성
app.config["BOARD_IMAGE_PATH"] = BOARD_IMAGE_PATH

# path가 없으면 path를 만드는 로직 추가
if not os.path.exists(app.config["BOARD_IMAGE_PATH"]):
    os.mkdir(app.config["BOARD_IMAGE_PATH"])


from . import make

