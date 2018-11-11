import datetime
import json
import re
import time
import websocket
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from flask import url_for
from flask import render_template
from flask_basicauth import BasicAuth
from os import environ

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
    return app

settings = utils.make_settings(environ.get('SETTINGS_FILE'))

app = create_app(settings)
app.app_context().push()

@app.route("/")
def index():
    return "OK"

@app.route("/login", methods = ['GET'])
@basic_auth.required
def login():
    now = datetime.datetime.utcnow()
    response = ("OK " + now.strftime("%Y-%m-%d %H:%M:%S"))
    return response

@app.route("/webhook", methods = ['GET', 'POST'])
def webhook():
    return "OK"
