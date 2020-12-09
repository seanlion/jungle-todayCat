from main import *

@app.route('/signup')
def registerPage():
    return render_template('signup.html')

@app.route('/signup', methods=["POST"])
def register():
    userList = mongo.db.users.find({}, {"_id":False})
    email_receive = request.form["emailText"]
    password1_receive = request.form["password1"]
    password2_receive = request.form["password2"]
    name_receive = request.form["nameTextarea"]
    # 받아온 정보가 빈칸이면 에러 메시지 반환
    if email_receive or password1_receive or password2_receive or name_receive is None:
        flash("입력이 완료되지 않았습니다.")
        return redirect(url_for("registerPage"))
    # email 중복 검사
    userEmails = userList["email"]
    if email_receive in userEmails:
        flash("이미 가입되어 있는 이메일입니다.", "error")
        return redirect(url_for("registerPage"))
    # password 일치 검사
    elif password1_receive != password2_receive:
        flash("비밀번호가 일치하지 않습니다.", "error")
        return redirect(url_for("registerPage"))
    else:
        password_hash = bcrypt.generate_password_hash(password1_receive)
        user = {"email": email_receive, "password": password_hash, "name": name_receive}
        mongo.db.users.insert_one(user)
        flash("회원가입이 완료되었습니다.")
        return redirect(url_for("loginPage"))