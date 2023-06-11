import os
from flask import Flask
from views import blue
from db import init_db
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# url
app.register_blueprint(blueprint=blue)

user = os.environ.get('USER')
pwd = os.environ.get('PWD')
host = os.environ.get('HOST')
dbn = os.environ.get('DBN')

# database
db_uri = f'mysql+pymysql://{user}:{pwd}@{host}:3306/{dbn}' # mysql+mysql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app=app)

# token
app.config['JWT_SECRET_KEY'] = 'wtkey'
jwt = JWTManager(app)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)