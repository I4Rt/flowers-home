from flask import Flask, request, json
from time import time
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bcrypt import Bcrypt


from flask_cors import CORS, cross_origin


# from flask_wtf.csrf import CSRFProtect

# csrf = CSRFProtect(app)

# from OpenSSL import SSL
# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')



app = Flask(__name__, template_folder='resources/templates',  static_folder='resources/static', static_url_path = '')

cors = CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})




bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost:5432/flowers_home'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


# app has been set and configured
Session(app)
db = SQLAlchemy(app)

