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
from flask_basicauth import BasicAuth
from os import environ
from database import db
from database import init_db
from database import DbTools
import utils
from urllib.parse import urlparse
from urllib.parse import parse_qs

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
    return app

settings = utils.make_settings(environ.get('SETTINGS_FILE'))

app = create_app(settings)
app.app_context().push()
db.init_app(app)
basic_auth = BasicAuth(app)
init_db(db)
database = DbTools(db)

def sanitize_coords(compass_coords):
    coords = []
    for i in compass_coords:
        if "N" in i:
            a = re.sub(r'N', '', i)
        elif "S" in i:
            a = re.sub(r'S', '-', i)
        elif "E" in i:
            a = re.sub(r'E', '', i)
        elif "W" in i:
            a = re.sub(r'W', '-', i)
        coords.append(a)
    return coords

def extract_coords(url):
    query = parse_qs(urlparse(url).query)
    compass_coords = query['q'][0].split(',')
    return compass_coords

@app.route("/")
def index():
    return "OK"

@app.route("/draw", methods = ['GET'])
@basic_auth.required
def draw():
    stored_coords = database.get_all_coords()
    return render_template('map.j2', coords=stored_coords, api_key=settings['gmaps_api_key'])

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
    gmap_url = incoming_sms['message'].split('\r')[-1]
    compass = extract_coords(gmap_url)
    if incoming_sms['sender'] == settings['tracker01']:
        tracker_label = 'Tracker01'
    elif incoming_sms['sender'] == settings['tracker02']:
        tracker_label = 'Tracker02'
    else:
        tracker_label = 'Unknown'

    coords = { 'compass': ",".join(compass),
               'computed_coords': ",".join(sanitize_coords(compass)),
               'tracker_label': tracker_label,
               'tracker_number': incoming_sms['sender'] }
    database.add_coords(coords)
    print(json.dumps(incoming_sms, sort_keys=True,
                     indent=4, separators=(',', ': ')))
    messages = database.get_all_messages()
    stored_coords = database.get_all_coords()
    for i in messages:
        print("Sender: " + i.sender)
        print("Recipient: " + i.recipient)
        print(i.message.split('\r'))
    for i in stored_coords:
        print("Compass: " + i.compass)
        print("Computed: " + i.computed_coords)
        print("Tracker Label: " + i.tracker_label)
        print("Tracker #: " + i.tracker_number)
        print("Timestamp: " + i.timestamp.isoformat())
    return "OK"
