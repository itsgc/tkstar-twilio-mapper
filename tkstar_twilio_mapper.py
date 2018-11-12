import datetime
import json
import re
import time
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from flask import url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_basicauth import BasicAuth
from os import environ
from database import db
from database import init_db
from database import DbTools
import utils

try:
    import thread
except ImportError:
    import _thread as thread
import time

def create_app(settings):
    app = Flask(__name__)
    app.config['SERVER_NAME'] = settings['server_fqdn']
    app.config['PREFERRED_URL_SCHEME'] = settings['url_scheme']
    app.config['BASIC_AUTH_USERNAME'] = settings['basic_auth_user']
    app.config['BASIC_AUTH_PASSWORD'] = settings['basic_auth_password']
    app.config['SQLALCHEMY_DATABASE_URI'] = settings['coords_db']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

settings = utils.make_settings(environ.get('SETTINGS_FILE'))

app = create_app(settings)
app.app_context().push()
basic_auth = BasicAuth(app)
init_db(db)
database = DbTools(db)

@app.route("/")
def index():
    return "OK"

@app.route("/draw", methods = ['GET'])
@basic_auth.required
def draw():
    return "OK"

@app.route("/login", methods = ['GET'])
@basic_auth.required
def login():
    now = datetime.datetime.utcnow()
    response = ("OK " + now.strftime("%Y-%m-%d %H:%M:%S"))
    return response

@app.route("/webhook", methods = ['POST'])
def webhook():
    incoming_sms = { 'message': request.values.get('Body', None),
                     'sender': request.values.get('From', None),
                     'recipient': request.values.get('To', None),
                     'id': request.values.get('SmsMessageSid', None) }
    database.add_message(incoming_sms)
    print(json.dumps(incoming_sms, sort_keys=True,
                     indent=4, separators=(',', ': ')))
    print(database.get_all_messages())
    return "OK"
