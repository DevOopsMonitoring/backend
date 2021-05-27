from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from src.api.schemas import SensorSchema
from src.models import Sensor
from src.extensions import db
from src.commons.pagination import paginate


class SensorResource(Resource):
    method_decorators = [jwt_required()]

    def get(self, sensor_id):
        schema = SensorSchema()
        sensor = Sensor.query.get_or_404(sensor_id)
        return {"sensor": schema.dump(sensor)}

    def put(self, sensor_id):
        schema = SensorSchema(partial=True)
        sensor = Sensor.query.get_or_404(sensor_id)
        sensor = schema.load(request.json, instance=sensor)

        db.session.commit()

        return {"msg": "Sensor updated", "sensor": schema.dump(sensor)}

    def delete(self, sensor_id):
        sensor = Sensor.query.get_or_404(sensor_id)
        db.session.delete(sensor)
        db.session.commit()

        return {"msg": "Sensor deleted"}


class SensorList(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        schema = SensorSchema(many=True)
        query = Sensor.query
        for key, item in request.args.items():
            query = query.filter(getattr(Sensor, key).like(item))
        return paginate(query, schema)

    def post(self):
        schema = SensorSchema()
        sensor = schema.load(request.json)

        db.session.add(sensor)
        db.session.commit()

        return {"msg": "Sensor created", "sensor": schema.dump(sensor)}, 201
