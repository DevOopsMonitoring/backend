from src.extensions import ma, db
from src.models import User
from .company import CompanySchema
from .position import PositionSchema
from .server import ServerSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    company = ma.Nested(CompanySchema, dump_only=True)
    position = ma.Nested(PositionSchema, dump_only=True)
    email = ma.Email()

    position_id = ma.Int(load_only=True)
    company_id = ma.Int(load_only=True)

    company_token = ma.String(load_only=True)

    servers = ma.Nested(ServerSchema, many=True, dump_only=True, exclude=('user', 'description', 'specifications'))
    servers_id = ma.List(ma.Int, load_only=True, default=[])
    servers_id_add = ma.List(ma.Int, load_only=True, default=[])

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password", )
