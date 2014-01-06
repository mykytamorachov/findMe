from app import db
from datetime import datetime
import re

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    account_type = db.Column(db.String(120), default='default')
    social_id = db.Column(db.Integer(120))
    social_network = db.Column(db.String(120))
    latitude = db.Column(db.Float(20))
    longitude = db.Column(db.Float(20))
    joined_date = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, name, username, email, password,
                 latitude, longitude, social_id, social_network):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.latitude = latitude
        self.longitude = longitude
        self.social_id = social_id
        self.social_network = social_network

    def __repr__(self):
        return "<User %r>" % self.username