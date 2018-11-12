from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Coords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compass = db.Column(db.Text)
    computed_coords = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    tracker_label = db.Column(db.Text)
    tracker_number = db.Column(db.Text)

    def __repr__(self):
        return '<Coords %r>' % self.compass

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messageid = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    sender = db.Column(db.Text)
    recipient = db.Column(db.Text)
    message = db.Column(db.Text)

    def __repr__(self):
        return '<Messages %r>' % self.messageid

def init_db(db):
    try:
        db.create_all()
        print("creating db...")
        db.session.commit()
    except Exception as e:
        error = "Failed creating the datatabase: {}".format(e)
        return error

class DbTools():
    def __init__(self, db):
        self.db = db
        self.now = datetime.datetime.utcnow()

    def get_all_messages(self):
        messages = Messages.query.all()
        return messages
    
    def get_all_coords(self):
        coords = Coords.query.all()
        return coords

    def add_coords(self, dict):
        new_entry = Coords(compass=dict['compass'], computed_coords=dict['computed_coords'],
                           timestamp=datetime.datetime.utcnow(),
                           tracker_label=dict['tracker_label'],
                           tracker_number=dict['tracker_number'])
        self.db.session.add(new_entry)
        self.db.session.commit()
        return True

    def add_message(self, dict):
        new_message = Messages(messageid=dict['id'],
                                 timestamp=datetime.datetime.utcnow(), sender=dict['sender'],
                                 recipient=dict['recipient'], message=dict['message'])
        self.db.session.add(new_message)
        db.session.commit()
