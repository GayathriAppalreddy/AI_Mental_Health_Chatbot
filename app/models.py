from . import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class MoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f"<MoodLog {self.id} {self.sentiment}>" 
