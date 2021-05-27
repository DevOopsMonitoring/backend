from src.extensions import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    address = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return f'<Company {self.name}>'
