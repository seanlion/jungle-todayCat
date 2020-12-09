from main import *


@app.route('/signup', methods=["GET","POST"])
def register():
    if request.method == ["POST"]:
        email_receive = request.form["email_give"]
        password_receive = request.form["password_give"]
        password_hash = bcrypt.generate_password_hash(password_receive)
        name_receive = request.form["name_give"]
        user = {"email": email_receive, "password": password_hash, "name": name_receive}
        mongo.db.users.insert_one(user)
        return jsonify({"result": "success"})
    else:
        userList = mongo.db.users.find({}, {"_id":False})
        return render_template('signup.html', userList = userList)

# @app.route('/signup', methods=["POST"])
# def ():
#     email_receive = request.form["email_give"]
#     password_receive = request.form["password_give"]
#     password_hash = bcrypt.generate_password_hash(password_receive)
#     name_receive = request.form["name_give"]
#     user = {"email": email_receive, "password": password_hash, "name": name_receive}
#     mongo.db.users.insert_one(user)
#     return jsonify({"result": "success"})