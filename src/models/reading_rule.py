from src.extensions import db


class ReadingRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    critical_value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<ReadingRule {self.sensor_id}-{self.server_id}, max: {self.critical_value}>'
