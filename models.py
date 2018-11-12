import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Coords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compass = db.Column(db.Text)
    computed_coords = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    tracker_label = db.Column(db.Text)
    tracker_number = db.Column(db.Text)

    def __init__(self, compass=None, computed_coords=None, timestamp=None,
                 tracker_label=None, tracker_number=None):
        self.compass = compass
        self.computed_coords = computed_coords
        self.timestamp = timestamp
        self.tracker_label = tracker_label
        self.tracker_number = tracker_number

    def __repr__(self):
        return '<Coords %r>' % self.compass

class SmsMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sms_message_id = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    sender = db.Column(db.Text)
    recipient = db.Column(db.Text)
    message = db.Column(db.Text)

    def __init__(self, sms_message_id=None, timestamp=None, sender=None,
                 recipient=None, message=None):
        self.sms_message_id = sms_message_id
        self.timestamp = timestamp
        self.sender = sender
        self.recipient = recipient
        self.message = message

    def __repr__(self):
        return '<SmsMessage %r>' % self.sms_message_id
