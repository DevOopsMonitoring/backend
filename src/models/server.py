from random import choices
from string import ascii_lowercase, digits
from .equipment import specifications

from src.extensions import db


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    address = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(16), nullable=False)
    reading_rules = db.relationship('ReadingRule', backref='server', lazy=True)
    read_data = db.relationship('ReadData', backref='server', lazy=True)
    specifications = db.relationship('Equipment', secondary=specifications, lazy='subquery', backref=db.backref('pages', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_token()

    def refresh_token(self):
        self.token = ''.join(choices(ascii_lowercase + digits, k=16))

    def __repr__(self):
        return f'<Server {self.name}>'
