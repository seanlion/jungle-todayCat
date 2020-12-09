from main import *

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/login', methods=["POST"])
def login():
    email = request.form.get("email")
    password = requeest.form.get("password")
    user = mongo.db.users.find_one({"email": email})
    user_password = user["password"]
    login_data = {'id':email, 'pass':password}
    login_url =
    if bcrypt.check_password_hash(user_password, password).decode('utf-8'):
        with requests Session() as s:
            res = s.post(LOGIN_URL: )