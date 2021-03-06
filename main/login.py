from main import *

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method =="POST":
        email = request.form.get("loginEmail")
        password = request.form.get("password")
        # db에 일치하는 이메일이 있는지 확인하고 user에 저장
        user = mongo.db.users.find_one({"email": email})
        # user가 None이라면 db에 일치하는 이메일이 없는것.
        if user is not None:
            # db에 저장되어있는 비밀번호 user_password 변수에 저장
            user_password = user["password"]
            print("email ok")
        else:

            flash("등록되지 않은 이메일입니다.")
            print("not email")
            return redirect(url_for("login"))

        # db에서 가져온 비밀번호는 해쉬화되어 있기 때문에 새로 가져온 비밀번호를 해쉬화해서 check_password_hash 메서드로 비교(True, False 반환)
        if bcrypt.check_password_hash(user_password, password):
            session.clear
            session["id"] = email
            session["name"] = user["name"]
            print(session)
            return redirect(url_for('index'))
        else:
            flash("비밀번호가 일치하지 않습니다.")
            print("password not ok")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    print(session)
    return redirect(url_for('index'))