from src.extensions import db


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    snmp = db.Column(db.String(127), nullable=False)
    reading_rules = db.relationship('ReadingRule', backref='sensor', lazy=True)
    read_data = db.relationship('ReadData', backref='sensor', lazy=True)

    def __repr__(self):
        return f'<Sensor {self.name}>'
