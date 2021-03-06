from flask import Flask,render_template,jsonify,request,session,redirect,url_for,send_from_directory,flash, get_flashed_messages
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from datetime import datetime,timezone,timedelta
import os,re, time,math,requests, random
from bson.objectid import ObjectId

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://jungle:jungle@3.35.207.236:27017/myDatabase?authSource=admin"
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

mongo = PyMongo(app)

bcrypt = Bcrypt(app)


BOARD_IMAGE_PATH = "/Users/seung/Desktop/backend/todaycat/images"
ALLOWED_EXTENSIONS = set(['png','pdf','jpg','JPG','JPEG', 'jpeg','gif'])

# 이미지 경로에 쉽게 접근하기 위해 환경 변수 생성
app.config["BOARD_IMAGE_PATH"] = BOARD_IMAGE_PATH
app.config["SECRET_KEY"] = "1jungle6"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(weeks=2)

# path가 없으면 path를 만드는 로직 추가
if not os.path.exists(app.config["BOARD_IMAGE_PATH"]):
    os.mkdir(app.config["BOARD_IMAGE_PATH"])


from . import make
from . import main
from . import delete
from . import signup
from . import login