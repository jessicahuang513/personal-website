from datetime import datetime
from app import db

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	content = db.Column(db.String)
	likes = db.Column(db.Integer, default=0)