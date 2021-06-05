from datetime import datetime

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from src.api.schemas import ReadingDataSchema
from src.extensions import db
from src.models import ReadData, ReadingRule, Server, User, Sensor
import requests
from os import getenv


def send_simple_message(email, server_name, value, sensor_name):
    domain = getenv('mailgun_domain')
    api = getenv('mailgun_api')

    return requests.post(
        f"https://api.mailgun.net/v3/{domain}.mailgun.org/messages",
        auth=("api", api),
        data={"from": f"Уведомление об ошибке <mailgun@{domain}.mailgun.org>",
              "to": [email],
              "subject": "Сервер в опасности!!!",
              "text": f"Внимание! \n\nСервер {server_name} в опасности! Поканазия с датчика {sensor_name} достигло значения {value}"})


class ReadDataResource(Resource):
    @jwt_required()
    def get(self, server_id):
        schema = ReadingDataSchema(many=True)
        data = ReadData.query.filter_by(server_id=server_id)
        tmp = {}
        for d in schema.dump(data):
            tmp[d['sensor']['name']] = {
                'critical_value': ReadingRule.query.filter_by(server_id=server_id, sensor_id=d['sensor']['id']).first().critical_value,
                'values': [dt.value for dt in data if dt.sensor_id == d['sensor']['id']][-40:],
                'time': [dt.data.strftime('%H:%M:%S') for dt in data if dt.sensor_id == d['sensor']['id']][:40],
            }

        result = []
        for k, v in tmp.items():
            result.append({'name': k} | v)
        return {"data": result}

    def post(self, server_token):
        server = Server.query.filter_by(token=server_token).first()
        if not server:
            return {'msg': 'Token not found'}, 403
        json = request.get_json()
        rule = ReadingRule.query.filter_by(server_id=server.id, sensor_id=json['sensor_id']).first()
        if not rule:
            return {"msg": "Reading rule not found"}, 404
        data = ReadData(data=datetime.now(), server_id=server.id, sensor_id=json['sensor_id'], value=json['value'])

        if json['value'] >= rule.critical_value:
            email = User.query.filter_by(id=server.user_id).first().email
            sensor_name = Sensor.query.filter_by(id=rule.sensor_id).first().name
            send_simple_message(email, server.name, json['value'], sensor_name)

        db.session.add(data)
        db.session.commit()

        return {"msg": "Data saves"}, 200


