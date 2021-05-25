from api.extensions import db


class Position(db.Model):
    name = db.Column(db.String(80), primary_key=True)

    def __repr__(self):
        return f'<Position {self.name}>'
