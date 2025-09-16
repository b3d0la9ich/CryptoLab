from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submissions = db.relationship('Submission', backref='author', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    algorithm = db.Column(db.String(50), nullable=False)  # 'caesar'|'vigenere'|'aes'|'rsa'
    payload = db.Column(db.Text, nullable=False)          # входные данные/задание
    answer_hash = db.Column(db.String(128), nullable=False)  # ожидаемый ответ (SHA-256)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)
    submitted_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    lab = db.relationship('Lab', backref='submissions')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
