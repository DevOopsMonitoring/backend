from random import choices
from string import ascii_lowercase, digits

from src.extensions import db


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    address = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(16), nullable=False)
    reading_rules = db.relationship('ReadingRule', backref='server', lazy=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_token()

    def refresh_token(self):
        self.token = ''.join(choices(ascii_lowercase + digits, k=16))

    def __repr__(self):
        return f'<Server {self.name}>'
