from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Coords
from models import SmsMessage
import datetime

db = SQLAlchemy()

def init_db(db):
    try:
        db.create_all()
        db.session.commit()
    except Exception as e:
        error = "Failed creating the datatabase: {}".format(e)
        return error

class DbTools():
    def __init__(self, db):
        self.db = db
        self.now = datetime.datetime.utcnow()

    def get_all_messages(self):
        messages = SmsMessage.query.all()
        return messages
    
    def get_all_coords(self):
        coords = Coords.query.all()
        return coords

    def add_cords(self, dict):
        new_entry = Coords(compass=dict['compass'], computed_coords=dict['computed_coords'],
                           timestamp=self.now,
                           tracker_label=dict['tracker_label'],
                           tracker_number=dict['tracker_number'])
        self.db.session.add(new_entry)
        self.db.session.commit()
        return True

    def add_message(self, dict):
        new_message = SmsMessage(sms_message_id=dict['id'],
                                 timestamp=self.now, sender=dict['sender'],
                                 recipient=dict['recipient'], message=dict['message'])
        self.db.session.add(new_message)
        db_session.commit()


