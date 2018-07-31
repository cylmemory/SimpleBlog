from .. import db, login_manager
from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

ROLES = (('admin', 'admin'), ('editor', 'editor'), ('writer', 'writer'), ('reader', 'reader'))
SOCIAL_NETWORKS = {
    'weibo': {'fa_icon': 'fa fa-weibo', 'url': None},
    'wechat': {'fa_icon': 'fa fa-wechat', 'url': None},
    'github': {'fa_icon': 'fa fa-github', 'url': None}
}


class User(UserMixin, db.Document):
    username = db.StringField(max_length=255, required=True)
    email = db.EmailField(max_length=255)
    password_hash = db.StringField(required=True)
    create_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    last_login_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    confirmed = db.BooleanField(default=False)
    role = db.StringField(max_length=32, default='reader', choices=ROLES)
    is_superuser = db.BooleanField(default=False)
    about_me = db.StringField()
    social_networks = db.DictField(default=SOCIAL_NETWORKS)
    homepage_url = db.URLField()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        try:
            return self.username
        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')


@login_manager.user_loader
def load_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user



