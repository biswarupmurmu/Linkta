from datetime import datetime
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(150), nullable=False)
    lname = db.Column(db.String(150))
    password = db.Column(db.String(150), nullable=False)
    contact_email = db.Column(db.String(120))
    whoami = db.Column(db.String(200), default = "")
    about = db.Column(db.String(1000), default = "")
    profile_picture = db.Column(db.String(250), default = "" )
    cover_picture = db.Column(db.String(250), default = "")
    public_view = db.Column(db.Boolean, default = False)
    date_added = db.Column(db.DateTime, default = datetime.now())