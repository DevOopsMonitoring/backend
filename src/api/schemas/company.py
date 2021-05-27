from src.models import Company
from src.extensions import ma, db


class CompanySchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)

    class Meta:
        model = Company
        sqla_session = db.session
        load_instance = True
