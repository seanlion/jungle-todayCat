from main import *
from string import digits, ascii_uppercase, ascii_lowercase

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/edit', methods=["POST"])
def edit_content():
    desc = request.form.get("desc")
    id = request.form.get("id")
    # updated = datetime.now(timezone.utc)
    filename = None
    print("desc:",desc)
    print("file_data:", request.files["new_attachfile"])
    file = request.files["new_attachfile"]
    if file and allowed_file(file.filename):
        filename = check_filename(file.filename)
        file.save(os.path.join(app.config["BOARD_IMAGE_PATH"],filename))
    print("filename:",filename)
    contents = mongo.db.contents
    # 추후에 session id 가 같은 유저만 수정 가능해야 함
    # data = contents.find_one({"_id": ObjectId(id)})
    contents.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"desc":desc, "attachfile": filename}}
    )
    return jsonify(data = "success")

@app.route('/', methods=["POST","GET"])
def write():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 5, type=int)
    contents = mongo.db.contents
    total_page_count = contents.find({}).count()
    last_page_num = math.ceil(total_page_count / limit)
    block_size = 5
    block_num = int((page - 1) / block_size)
    block_start = int((block_size * block_num) + 1)
    block_last = math.ceil(block_start + (block_size - 1))

    created = round(datetime.utcnow().timestamp() * 1000)
    contents = mongo.db.contents

    if request.method == "POST":
        desc = request.form.get("desc")
        filename = None
        # form에서 넘어온 파일이 있냐를 체크해야함.(name의 값을 이용)
        if "attachfile" in request.files:
            file = request.files["attachfile"]
            # 원본 filename이 제대로 된 파일이름(확장자)을 가졌는지 확인
            if file and allowed_file(file.filename):
                # 새로운 파일네임을 만드는 함수를 실행시킴.
                filename = check_filename(file.filename)
                file.save(os.path.join(app.config["BOARD_IMAGE_PATH"], filename))

        post = {
            "desc": desc,
            "created": created,
            "attachfile": filename,
            "writer_id": session.get("id")
        }
        x = contents.insert_one(post)
        results = contents.find({})
        return render_template('home.html',results=results,limit=limit, page=page, block_start=block_start,
                               block_last=block_last, last_page_num=last_page_num)
    else:
        results = contents.find({}).skip((page - 1) * limit).limit(limit).sort("created", -1)
        return render_template('home.html', results=results, limit=limit, page=page, block_start=block_start,
                               block_last=block_last, last_page_num=last_page_num)

@app.route('/photos', methods=["POST"])
def random_photo():
    files = os.listdir(BOARD_IMAGE_PATH)
    d = random.choice(files)
    print("random_photo:",d)
    return url_for('uploaded_file',filename=d)

@app.route("/images/<filename>")
def uploaded_file(filename):
    print("uploaded file 함수 접속.")
  # WYSWIG 강의의 28분 구간을 참조.
    result = send_from_directory(app.config["BOARD_IMAGE_PATH"], filename)
    print("result:",result)
    return send_from_directory(app.config["BOARD_IMAGE_PATH"], filename)

def allowed_file(filename):
      # 파일 명에 확장자가 '.'으로 구분되니까 그 '.'이 있는지 찾는거고, rsplit을 하면 구분자를 기준으로 맨 오른쪽에서부터 1개를 자르는 것. 그럼 2개의 문자열이 리스트로 나옴. 그 리스트 index의 1번째 요소가 ALLOWED~에 있는지 확인
      return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS

def random_generator(length=8):
      # 소문자,대문자,숫자가 다 담겨짐..
      char = digits + ascii_lowercase + ascii_uppercase
      # 문자열 형태로 리턴
      return "".join(random.sample(char,length))

# 파일 첨부 기능에 대한 코드 추가 : flask의 secure_filename을 못 쓰는 대신(파일명이 한글도 있을텐데 저건 ascii 문자만 취급) 직접 변형해서 만드려고 함.
def check_filename(filename):
    reg= re.compile("[^A-Za-z0-9_.가-힝-]")
      # 한글 문자 경로와 ascii 문자 경로를 os.path.sep, altsep로 커버 가능.
    for s in os.path.sep, os.path.altsep:
        if s:
          filename = filename.replace(s, " ")
          # 공백을 기준으로 split되어 리스트에 담기는 데 그걸 공백 자리에 '_'를 넣어 다시 하나의 문자열로 만든다. 그리고 위에 reg에서 정의한 패턴(영문,한글,숫자,대시 등등이 아닌 문자)과 일치하다면 그 부분을 공백으로 만들어라. 그리고 그걸 문자열로 치환하고 "._"는 없애버리기. 기대결과는 경로로 들어오는 문자열 중 '.'이나 '/'같은거 다 없애고 하나의 문자열로 만드는것!
          filename= str(reg.sub('', '_'.join(filename.split()))).strip("._")
    return filename


@app.template_filter('format_datetime')
def format_datetime(ts):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    ts = datetime.fromtimestamp((int(ts)/1000)) + offset
    return ts.strftime('%Y-%m-%d')