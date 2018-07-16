from .. import db
from flask_login import UserMixin
import datetime

Roles = (('admin', 'admin'), ('editor', 'editor'), ('writer', 'writer'), ('reader', 'reader'))


class User(UserMixin, db.Document):
    username = db.StingField(max_length=255, required=True)
    email = db.EmailField(max_length=255)
    password_hash = db.StringField(required=True)
    create_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    last_login_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    confirmed = db.BooleanField(required=False)
    role = db.StringField(max_length=32, default='reader', choices=Roles)




