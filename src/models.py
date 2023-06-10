from .db import db
from uuid import uuid1
from datetime import datetime

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