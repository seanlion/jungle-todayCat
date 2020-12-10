from main import *

@app.route('/mypage', methods=['GET'])
def mypage():
    if session.get('id') is None or session.get('id') == "":
        # connection reset 에러 해결. 발표 때 얘기하기
        flash("로그인해주세요.")
        return redirect(url_for('login'))
    else:
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 5, type=int)
        contents = mongo.db.contents
        id_receive = session.get("id")
        total_page_count = contents.find({'writer_id':id_receive}).count()
        last_page_num = math.ceil(total_page_count / limit)
        block_size = 5
        block_num = int((page - 1) / block_size)
        block_start = int((block_size * block_num) + 1)
        block_last = math.ceil(block_start + (block_size - 1))
        results = contents.find({'writer_id':id_receive}).skip((page - 1) * limit).limit(limit).sort("created", -1)
        return render_template('/mypage.html', results=results,limit=limit, page=page, block_start=block_start,
                                   block_last=block_last, last_page_num=last_page_num)
