from datetime import datetime
from app import db
from hashlib import md5
from werkzeug.security import generate_password_hash, \
    check_password_hash
from flask_login import UserMixin
from app import db, login
from flask import current_app

followers = db.Table('followers', db.Column('follower_id', db.Integer,
                     db.ForeignKey('user.id')), db.Column('followed_id'
                     , db.Integer, db.ForeignKey('user.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(25), default="ADMIN")
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=followers.c.follower_id == id,
        secondaryjoin=followers.c.followed_id == id,
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic',
        )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def active(self):
        return self.last_seen.strftime("%H:%M:%S") == datetime.utcnow().strftime("%H:%M:%S")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# def avatar(self, size):
#     digest = md5(self.email.lower().encode('utf-8')).hexdigest()
#     return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}' \
#     .format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id
                                    == user.id).count() > 0

# def get_reset_password_token(self, expires_in=600):
#     return jwt.encode({'reset_password': self.id, 'exp': time()
#                       + expires_in}, current_app.config['SECRET_KEY'],
#                       algorithm='HS256').decode('utf-8')

# @staticmethod
# def verify_reset_password_token(token):
#     try:
#         id = jwt.decode(token, current_app.config['SECRET_KEY'],
#                         algorithms=['HS256'])['reset_password']
#     except:
#         return
#     return User.query.get(id)

@staticmethod
def get_user_count():
    return User.query.all().count()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	description = db.Column(db.String(1000))
	body = db.Column(db.String(100000))
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)