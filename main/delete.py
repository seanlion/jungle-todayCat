from main import *

@app.route('/delete/<_id>')
def delete(_id):
    contents = mongo.db.contents
    print(type(ObjectId(_id)))
    contents.find_one_and_delete({"_id": ObjectId(_id)})
    return redirect(url_for('mypage'))
