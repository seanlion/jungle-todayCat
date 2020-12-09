from main import *


@app.route('/signup', methods=["GET","POST"])
def register():
    if request.method == "POST":
        userList = list(mongo.db.users.find({}, {"_id":False}))
        email_receive = request.form["emailText"]
        password1_receive = request.form["password1"]
        password2_receive = request.form["password2"]
        name_receive = request.form["nameTextarea"]
        # 받아온 정보가 빈칸이면 에러 메시지 반환
        print(email_receive, password1_receive, password2_receive, name_receive)
        if email_receive == "" or password1_receive == "" or password2_receive == "" or name_receive == "":
            print("not insert")
            flash("빈칸이 남아 있습니다.")
            return redirect(url_for("register"))
        # email 중복 검사
        for index in range(len(userList)):
            if email_receive == userList[index]["email"]:
                print("already register")
                flash("이미 가입되어 있는 이메일입니다.")
                return redirect(url_for("register"))
        # password 일치 검사
        if password1_receive != password2_receive:
            print("discord")
            flash("비밀번호가 일치하지 않습니다.")
            return redirect(url_for("register"))
        else:
            password_hash = bcrypt.generate_password_hash(password1_receive)
            user = {"email": email_receive, "password": password_hash, "name": name_receive}
            mongo.db.users.insert_one(user)
            flash("환영합니다! 오늘의 고양이 집사가 되셨습니다.")
            return redirect(url_for("login"))
    else :
        return render_template('signup.html')