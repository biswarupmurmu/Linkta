from datetime import datetime
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(150), nullable=False)
    lname = db.Column(db.String(150))
    password = db.Column(db.String(150), nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.now())