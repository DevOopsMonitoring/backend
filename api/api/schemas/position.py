from api.models import Position
from api.extensions import ma, db


class PositionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Position
        sqla_session = db.session
        load_instance = True
