from main import *
from flask_bcrypt import Bcrypt

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/signup', methods=["GET"])
def index():
    userList = mongo.db.users.find({}, {"_id":False})
    return render_template('signup.html'), jsonify({"list":userList})

@app.route('/signup', methods=["POST"])
def register():
    email_receive = request.form["email_give"]
    password_receive = request.form["password_give"]
    password_hash = bcrypt.generate_password_hash(password_receive)
    name_receive = request.form["name_give"]
    doc = {"email": email_receive, "password": password_hash, "name": name_receive}
    mongo.db.users.insert_one(doc)
    return jsonify({"result": "success"})