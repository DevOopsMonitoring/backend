from api.models import Server
from api.extensions import ma, db


class ServerSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    token = ma.Str(dump_only=True)

    class Meta:
        model = Server
        sqla_session = db.session
        load_instance = True
