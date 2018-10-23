from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

ROLES = (('admin', 'admin'), ('editor', 'editor'), ('writer', 'writer'), ('reader', 'reader'))
SOCIAL_NETWORKS = {
    'weibo': {'fa_icon': 'fa fa-weibo', 'url': None},
    'wechat': {'fa_icon': 'fa fa-weixin', 'url': None},
    'github': {'fa_icon': 'fa fa-github', 'url': None},
    'twitter': {'fa_icon': 'fa fa fa-twitter', 'url': None},
    'facebook': {'fa_icon': 'fa fa-facebook', 'url': None},
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
    confirm_send_time = db.DateTimeField()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.username})

    def confirm_email(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('confirm') != self.username:
            return False
        self.confirmed = True
        self.save()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.username})

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)

        except Exception:
            return False

        try:
            user = User.objects.get(username=data.get('reset'))

        except Exception:
            return False

        user.password = new_password
        user.save()

        return True

    def get_id(self):
        try:
            return self.username
        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')

    def user_to_dict(self):
        dict_user = {}

        dict_user['username'] = self.username
        dict_user['email'] = self.email
        dict_user['confirmed'] = self.confirmed
        dict_user['role'] = self.role
        dict_user['is_superuser'] = self.is_superuser
        dict_user['about_me'] = self.about_me
        dict_user['social_networks'] = self.social_networks
        dict_user['about_me'] = self.about_me
        dict_user['last_login_time'] = self.last_login_time.strftime('%Y-%m-%d %H:%M')
        dict_user['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M')
        dict_user['confirm_send_time'] = self.confirm_send_time.strftime('%Y-%m-%d %H:%M')

        return dict_user

    def __unicode__(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user



