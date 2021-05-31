from src.extensions import ma, db
from src.models import ReadData
from .sensor import SensorSchema
from .server import ServerSchema


class ReadingDataSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    server = ma.Nested(ServerSchema)
    sensor = ma.Nested(SensorSchema)
    date = ma.DateTime(dump_only=True)

    sensor_id = ma.Int(load_only=True)
    server_id = ma.Int(load_only=True)

    class Meta:
        model = ReadData
        sqla_session = db.session
        load_instance = True
