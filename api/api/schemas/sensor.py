from api.models import Sensor
from api.extensions import ma, db


class SensorSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)

    class Meta:
        model = Sensor
        sqla_session = db.session
        load_instance = True
