from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from api.api.schemas import UserSchema
from api.models import User
from api.extensions import db
from api.commons.pagination import paginate


class UserResource(Resource):
    method_decorators = [jwt_required()]

    def get(self, user_id):
        schema = UserSchema()
        user = User.query.get_or_404(user_id)
        return {"user": schema.dump(user)}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)

        db.session.commit()

        return {"msg": "user updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"msg": "user deleted"}


class UserList(Resource):

    @jwt_required()
    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        for key, item in request.args.items():
            query = query.filter(getattr(User, key).like(item))
        return paginate(query, schema)

    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)

        db.session.add(user)
        db.session.commit()

        return {"msg": "user created", "user": schema.dump(user)}, 201
