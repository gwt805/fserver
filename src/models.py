from .db import db
from uuid import uuid1

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid1()))
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=True)
    img = db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return self.username