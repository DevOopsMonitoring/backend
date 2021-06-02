from src.models import Server
from src.extensions import ma, db
from .equipment import EquipmentSchema


class ServerSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    token = ma.Str(dump_only=True)
    specifications = ma.Nested(EquipmentSchema, many=True, dump_only=True)
    specifications_id = ma.List(ma.Int, load_only=True)

    class Meta:
        model = Server
        sqla_session = db.session
        load_instance = True
        include_fk = True
