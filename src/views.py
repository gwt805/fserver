from .models import *
from flask import Blueprint
from sqlalchemy.exc import DatabaseError
import hashlib

# 密码加密
def hash_code(s):  # 加点盐
    h = hashlib.sha256()
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

blue = Blueprint('api', __name__)

@blue.route('/')
def index():
    return 'hello world'

@blue.route('/useradd', methods=['POST'])
def useradd():
    user = User()
    user.username = 'admin'
    user.password = hash_code('admin')
    user.email = 'admin@admin.com'
    try:
        db.session.add(user)
        db.session.commit()
    except DatabaseError as e:
        print(e)
        db.session.rollback()
        db.session.flush()
    # 多条数据 [] db.session.add_all([]) db.session.commit()
    return 'success'

@blue.route('/userdel', methods=['DELETE'])
def userdelete():
    user = User.query.first()
    try:
        db.session.delete(user)
        db.session.commit()
    except DatabaseError as e:
        print(e)
        db.session.rollback()
        db.session.flush()
    return 'success'

@blue.route('/userupd', methods=['PUT'])
def userupd():
    user = User.query.first()
    user.email = "admin@qq.com"
    try:
        db.session.add(user)
        db.session.commit()
    except DatabaseError as e:
        print(e)
        db.session.rollback()
        db.session.flush()
    return 'success'

@blue.route('/usersearch', methods=['GET'])
def usersearch():
    user = User.query.paginate(page=1, per_page=10, error_out=False)
    print(list(user))
    return 'success'