from src.extensions import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FIO = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Order {self.id}>'
