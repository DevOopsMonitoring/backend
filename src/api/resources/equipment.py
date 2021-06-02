from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from src.api.schemas import EquipmentSchema
from src.commons.pagination import paginate
from src.extensions import db
from src.models import Equipment


class EquipmentResource(Resource):
    method_decorators = [jwt_required()]

    def get(self, equipment_id):
        schema = EquipmentSchema()
        equipment = Equipment.query.get_or_404(equipment_id)
        return {"equipment": schema.dump(equipment)}

    def put(self, equipment_id):
        schema = EquipmentSchema(partial=True)
        equipment = Equipment.query.get_or_404(equipment_id)
        equipment = schema.load(request.json, instance=equipment)

        db.session.commit()

        return {"msg": "Equipment updated", "equipment": schema.dump(equipment)}

    def delete(self, equipment_id):
        equipment = Equipment.query.get_or_404(equipment_id)
        db.session.delete(equipment)
        db.session.commit()

        return {"msg": "Equipment deleted"}


class EquipmentList(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        schema = EquipmentSchema(many=True)
        query = Equipment.query
        for key, item in request.args.items():
            query = query.filter(getattr(Equipment, key).like(item))
        return paginate(query, schema)

    def post(self):
        schema = EquipmentSchema()
        equipment = schema.load(request.json)

        db.session.add(equipment)
        db.session.commit()

        return {"msg": "Equipment created", "equipment": schema.dump(equipment)}, 201
