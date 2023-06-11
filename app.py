import os
import json
import hashlib
from uuid import uuid1
from flask import Flask
from loguru import logger
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError
from flask_jwt_extended import JWTManager
from jinja2.exceptions import TemplateNotFound
from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import create_access_token, jwt_required

app = Flask(__name__)

user = os.environ.get('USER')
pwd = os.environ.get('PWD')
host = os.environ.get('HOST')
dbn = os.environ.get('DBN')

# database
db = SQLAlchemy()
migrate = Migrate()
#db_uri = f'mysql+pymysql://{user}:{pwd}@{host}:3306/{dbn}' # mysql+mysql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///fserver.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app=app)
migrate.init_app(app=app, db=db)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid1()), comment="UUID")
    nickname = db.Column(db.String(255), nullable=False, comment="昵称")
    username = db.Column(db.String(255), nullable=False, unique=True, comment="账号")
    password = db.Column(db.String(255), nullable=False, comment="密码")
    email = db.Column(db.String(255), nullable=False, unique=True, comment="邮箱")
    description = db.Column(db.String(1024), nullable=True, comment="简介")
    isadmin = db.Column(db.Boolean, nullable=False, default=False, comment="是否是管理员")
    key = db.Column(db.String(20), nullable=False, default=str(uuid1().hex)[:-12], comment="Key")
    img = db.Column(db.String(1024), nullable=True, comment="头像")
    createdate = db.Column(db.Date, nullable=False, default=datetime.now().strftime("%Y-%m-%d"), comment="创建时间")
    lastlogin = db.Column(db.Date, nullable=True, comment="最后登录时间")

    def __repr__(self):
        return self.username

# token
app.config['JWT_SECRET_KEY'] = 'wtkey'
jwt = JWTManager(app)



# 密码加密
def hash_code(s):  # 加点盐
    h = hashlib.sha256()
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

blue = Blueprint('wtapi', __name__)

@blue.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@blue.route('/', methods=['GET'])
@blue.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@blue.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@blue.route('/apis/<string:api>', methods=['GET'])
def apis(api):
    try:
        return render_template(f'{api}.html')
    except TemplateNotFound as e:
        return '<h1 style="text-align:center;font-size:48px;">404 Not Found</h1>'

@blue.route('/api/register', methods=['POST'])
def api_register():
    user = User()
    data = json.loads(request.get_data())
    nickname = data["nickname"]
    username = data["username"]
    password = data["password"]
    email = data["email"]
    logger.info(f"nick: {nickname} user: {username} password: {password}, email: {email}")
    user.nickname = nickname
    user.username = username
    user.password = hash_code(password)
    user.email = email
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"code": 0, "msg": "注册成功!"})
    except DatabaseError as e:
        logger.error(e)
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": -1, "msg": "注册失败!"})

@blue.route('/api/login', methods=['POST'])
def api_login():
    import datetime
    data = json.loads(request.get_data())
    username = data["username"]
    password = data["password"]
    info = User.query.filter_by(username=username).first()
    if info == None:
        return jsonify({"code": -1, "msg": "用户名不存在!"})
    else:
        if info.password == hash_code(password):
            access_token = create_access_token(identity = info.id, expires_delta=datetime.timedelta(days=7))
            return jsonify({"code": 0, "msg": "登录成功!", "data": {'nickname': info.nickname, "username": info.username, "img": info.img, "access_token": "Bearer "+access_token}})
        else:
            return jsonify({"code": -1, "msg": "密码错误!"})

@blue.route('/api/userinfo/<string:user>', methods=['GET'])
@jwt_required()
def userinfo(user):
    info = User.query.filter_by(username = user).first()
    info_dict = {
        "img": info.img,
        "nickname": info.nickname,
        "username": info.username,
        "isadmin": info.isadmin,
        "email": info.email,
        "key": info.key,
        "description": info.description
    }
    return jsonify({"code": 0, "msg": "查询成功!", "data": info_dict})

@blue.route('/api/userupd/<string:user>', methods=['PUT'])
@jwt_required()
def userupd(user):
    data = json.loads(request.get_data())
    img = data['img']
    nickname = data['nickname']
    email = data['email']
    description = data['description']

    userupd = User.query.filter_by(username = user).first()
    userupd.img = img
    userupd.nickname = nickname
    userupd.email = email
    userupd.description = description

    try:
        db.session.add(userupd)
        db.session.commit()
        return jsonify({"code": 0, "msg": "修改成功!", "data": {'img': img, 'nickname': nickname}})
    except DatabaseError as e:
        logger.error(e)
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": -1, "msg": "修改失败!"})

@blue.route('/api/userupdpwd/<string:user>', methods=['PUT'])
@jwt_required()
def userupdpwd(user):
    data = json.loads(request.get_data())
    password = data['password']

    userupd = User.query.filter_by(username = user).first()
    userupd.password = hash_code(password)

    try:
        db.session.add(userupd)
        db.session.commit()
        return jsonify({"code": 0, "msg": "修改成功!"})
    except DatabaseError as e:
        logger.error(e)
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": -1, "msg": "修改失败!"})


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)