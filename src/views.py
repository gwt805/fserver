import json
import hashlib
from .models import *
from loguru import logger
from flask import request, jsonify, render_template, Blueprint
from sqlalchemy.exc import DatabaseError
from jinja2.exceptions import TemplateNotFound

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
    data = json.loads(request.get_data())
    username = data["username"]
    password = data["password"]
    info = User.query.filter_by(username=username).first()
    if info == None:
        return jsonify({"code": -1, "msg": "用户名不存在!"})
    else:
        if info.password == hash_code(password):
            return jsonify({"code": 0, "msg": "登录成功!", "data": {'nickname': info.nickname, 'username': info.username, "img": info.img}})
        else:
            return jsonify({"code": -1, "msg": "密码错误!"})

@blue.route('/api/userinfo/<string:user>', methods=['GET'])
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