import bcrypt as bcrypt
from sqlalchemy import *
from flask import *
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from flask_swagger_ui import *
from main import *
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import and_
app = Flask(__name__)