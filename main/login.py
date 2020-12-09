from main import *

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/login')
def loginPage():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login():
    email = request.form.get("loginEmail")
    password = request.form.get("password")
    # db에 일치하는 이메일이 있는지 확인하고 user에 저
    user = mongo.db.users.find_one({"email": email})장
    # user가 None이라면 db에 일치하는 이메일이 없는것.
    if user is not None:
        # db에 저장되어있는 비밀번호 user_password 변수에 저장
        user_password = user["password"]
    else:
        flash({"msg": "이메일이 일치하지 않습니다."})
        return redirect(url_for("loginPage"))
    login_data = {'id':email, 'pass':password}
    login_url = "/login"
    # db에서 가져온 비밀번호는 해쉬화되어 있기 때문에 새로 가져온 비밀번호를 해쉬화해서 check_password_hash 메서드로 비교(True, False 반환)
    if bcrypt.check_password_hash(user_password, password).decode('utf-8'):
        # with as 구문으로 세션 구동 -> 브라우저 종료시까지 유지
        with requests.Session() as s:
            # login_data를 data에 담아 포스트 -> 세션에 넣어줌
            res = s.post(LOGIN_URL= login_url, data= login_data, verify=False, allow_redirects=False)
        return redirect(url_for("write"))
    else:
        flash("msg": "비밀번호가 일치하지 않습니다.")
        return redirect(url_for("loginPage"))