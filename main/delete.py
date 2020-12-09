from main import *

import requests
from flask_pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.myDatabase

@bp.route('/delete/<_id>', methods=('GET','POST'))
def delete(_id):
    if request.method == 'POST':
        contents_id = request.contents._id
        contents.remove({"_id": contents_id})
        return redirect('/mypage')
    else:
        contents_id = request.contents._id
        post = contents.find_one({"_id": contents_id})
        return render_template('mypage.html', post=post)