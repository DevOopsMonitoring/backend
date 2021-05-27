from src.models import Position
from src.extensions import ma, db


class PositionSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)

    class Meta:
        model = Position
        sqla_session = db.session
        load_instance = True
