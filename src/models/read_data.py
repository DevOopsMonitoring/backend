from src.extensions import db


class ReadData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<ReadData {self.sensor_id}-{self.server_id}, max: {self.critical_value}>'
