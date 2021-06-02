from src.models import Equipment
from src.extensions import ma, db


class EquipmentSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)

    class Meta:
        model = Equipment
        sqla_session = db.session
        load_instance = True
