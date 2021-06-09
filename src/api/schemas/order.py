from src.models import Order
from src.extensions import ma, db


class OrderSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    email = ma.Email()

    class Meta:
        model = Order
        sqla_session = db.session
        load_instance = True
        include_fk = True
