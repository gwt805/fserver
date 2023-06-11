import json
import hashlib
from models import *
from loguru import logger
from sqlalchemy.exc import DatabaseError
from jinja2.exceptions import TemplateNotFound
from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import create_access_token, jwt_required


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
