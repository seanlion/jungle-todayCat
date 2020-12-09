from main import *


@app.route('/signup', methods=["GET","POST"])
def register():
    if request.method == "POST":
        userList = mongo.db.users.find({}, {"_id":False})
        email_receive = request.form["emailText"]
        password1_receive = request.form["password1"]
        password2_receive = request.form["password2"]
        name_receive = request.form["nameTextarea"]

        password_hash = bcrypt.generate_password_hash(password1_receive)
        user = {"email": email_receive, "password": password_hash, "name": name_receive}
        mongo.db.users.insert_one(user)
        flash("회원가입이 완료되었습니다.")
        return redirect(url_for("login"))
    else :
        return render_template('signup.html')