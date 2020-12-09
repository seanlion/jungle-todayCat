from main import *

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/login', methods=["POST"])
def login():
    email = request.form.get("email_give")
    password = request.form.get("password_give")
    user = mongo.db.users.find_one({"email": email})
    if user:
        user_password = user["password"]
    else:
        return jsonify({"result": "fail", "msg": "이메일이 일치하지 않습니다."})
    login_data = {'id':email, 'pass':password}
    login_url = "/login"
    if bcrypt.check_password_hash(user_password, password).decode('utf-8'):
        with requests.Session() as s:
            res = s.post(LOGIN_URL= login_url, data= login_data, verify=False, allow_redirects=False)
            redirect_cookie = res.headers["Set-Cookie"]
            redirect_url = res.headers["Location"]
            headers = {"Cookie": redirect_cookie}

            s.get(redirect_url, headers=headers)
        redirect('/get')
        return jsonify({"result": "success"})
    else:
        return jsonify({"result": "fail", "msg": "비밀번호가 일치하지 않습니다."})
