from api.models import Company
from api.extensions import ma, db


class CompanySchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)

    class Meta:
        model = Company
        sqla_session = db.session
        load_instance = True
