from flask import Flask
from .views import blue
from .db import init_db
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# url
app.register_blueprint(blueprint=blue)

# database
db_uri = 'mysql+pymysql://root:200805@localhost:3306/test' # mysql+mysql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app=app)