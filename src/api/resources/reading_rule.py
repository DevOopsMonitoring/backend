from pprint import pprint

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from src.api.schemas import ReadingRuleSchema
from src.commons.pagination import paginate
from src.extensions import db
from src.models import ReadingRule, Server, Sensor


class ReadingRuleResource(Resource):
    def get(self, server_token):
        schema = ReadingRuleSchema(many=True, exclude=['server'])
        server = Server.query.filter_by(token=server_token).first()
        rules = ReadingRule.query.filter_by(server_id=server.id)
        snmp = []
        for rule in rules:
            snmp.append({
                'snmp': rule.sensor.snmp,
                'sensor_id': rule.sensor.id
            })
        return {"rules": snmp}

    @jwt_required()
    def put(self, rule_id):
        schema = ReadingRuleSchema(partial=True)
        rule = ReadingRule.query.get_or_404(rule_id)
        rule = schema.load(request.json, instance=rule)

        db.session.commit()

        return {"msg": "Reading rule updated", "rule": schema.dump(rule)}

    @jwt_required()
    def delete(self, rule_id):
        rule = ReadingRule.query.get_or_404(rule_id)
        db.session.delete(rule)
        db.session.commit()

        return {"msg": "Reading rule deleted"}


class ReadingRuleList(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        schema = ReadingRuleSchema(many=True)
        query = ReadingRule.query
        for key, item in request.args.items():
            query = query.filter(getattr(ReadingRule, key).like(item))
        return paginate(query, schema)

    def post(self):
        schema = ReadingRuleSchema()
        rule = schema.load(request.json)

        if not Sensor.query.filter_by(id=rule.sensor_id):
            return {'error': 'Sensor not found'}, 404

        if not Server.query.filter_by(id=rule.server_id):
            return {'error': 'Server not found'}, 404

        db.session.add(rule)
        db.session.commit()

        return {"msg": "Reading rule created", "rule": schema.dump(rule)}, 201
