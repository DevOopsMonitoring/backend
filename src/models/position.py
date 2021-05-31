from src.extensions import db


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='position', lazy=True)

    def __repr__(self):
        return f'<Position {self.name}>'
