from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from api.api.schemas import PositionSchema
from api.models import Position
from api.extensions import db
from api.commons.pagination import paginate


class PositionResource(Resource):
    method_decorators = [jwt_required()]

    def get(self, position_id):
        print(position_id)
        schema = PositionSchema()
        position = Position.query.get_or_404(position_id)
        return {"position": schema.dump(position)}

    def put(self, position_id):
        schema = PositionSchema(partial=True)
        position = Position.query.get_or_404(position_id)
        position = schema.load(request.json, instance=position)

        db.session.commit()

        return {"msg": "Position updated", "position": schema.dump(position)}

    def delete(self, position_id):
        position = Position.query.get_or_404(position_id)
        db.session.delete(position)
        db.session.commit()

        return {"msg": "Position deleted"}


class PositionList(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        schema = PositionSchema(many=True)
        query = Position.query
        for key, item in request.args.items():
            query = query.filter(getattr(Position, key).like(item))
        return paginate(query, schema)

    def post(self):
        schema = PositionSchema()
        position = schema.load(request.json)

        db.session.add(position)
        db.session.commit()

        return {"msg": "Position created", "position": schema.dump(position)}, 201
