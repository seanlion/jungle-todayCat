from main import *

# import requests
from flask_pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.myDatabase


@app.route('/mypage', methods=['GET'])
def mypage():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 5, type=int)
    contents = mongo.db.contents
    total_page_count = contents.find({}).count()
    last_page_num = math.ceil(total_page_count / limit)
    block_size = 5
    block_num = int((page - 1) / block_size)
    block_start = int((block_size * block_num) + 1)
    block_last = math.ceil(block_start + (block_size - 1))
    id_receive = session.get("id")
    results = db.contents.find({'writer_id':id_receive}).skip((page - 1) * limit).limit(limit).sort("created", -1)
    return render_template('/mypage.html', results=results,limit=limit, page=page, block_start=block_start,
                               block_last=block_last, last_page_num=last_page_num)
