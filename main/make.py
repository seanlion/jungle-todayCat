from main import *
from string import digits, ascii_uppercase, ascii_lowercase

@app.route('/write', methods=["POST"])
def write():
    if request.method == "POST":
        desc = request.form.get("desc")
        created = datetime.now(timezone.utc)
        print("created:", created)
        filename = None
        for k in request.files:
            print("file test", k)
        # form에서 넘어온 파일이 있냐를 체크해야함.(name의 값을 이용)
        if "attachfile" in request.files:
            file = request.files["attachfile"]
            print("file:",file)
            # 원본 filename이 제대로 된 파일이름(확장자)을 가졌는지 확인
            if file and allowed_file(file.filename):
                # 새로운 파일네임을 만드는 함수를 실행시킴.
                filename = check_filename(file.filename)
                file.save(os.path.join(app.config["BOARD_IMAGE_PATH"], filename))

        contents = mongo.db.contents
        post = {
            "desc" : desc,
            "created" : created,
            "attachfile": filename,
            "writer_id" : session.get("id")
        }

        x = contents.insert_one(post)
        return redirect(url_for('write',idx=x.inserted_id))

        # return redirect(request.url)
    else:
        contents = mongo.db.contents
        # data = contents.find_one({"_id": ObjectId(idx)})
        # print("data:", data)
        # result = {
        #     "id": data.get("_id"),
        #     "desc": data.get("desc"),
        #     "writer_id": data.get("writer_id", ""),
        #     "attachfile": data.get("attachfile", "")
        # }

        return render_template("mypage.html")

@app.route("/upload_image", methods=["POST"])
def upload_image():
    if request.method == "POST":
        # write.html의 uploadImage 함수 내용 중 image 인자를 image라는 이름으로 append함. 여기서 image가 그 image.
        file = request.files["image"]
        if file and allowed_file(file.filename):
          filename = "{}.jpg".format(random_generator())
          savefilepath = os.path.join(app.config["BOARD_IMAGE_PATH"], filename)
          file.save(savefilepath)
          return url_for("board.board_images", filename=filename)

@app.route("/images/<filename>")
def uploaded_file(filename):
  # WYSWIG 강의의 28분 구간을 참조.
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