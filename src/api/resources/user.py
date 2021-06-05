from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from src.api.schemas import UserSchema
from src.models import User, Server, Company
from src.extensions import db
from src.commons.pagination import paginate


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

        if hasattr(user, 'servers_id_add'):
            user.servers += Server.query.filter(Server.id.in_(user.servers_id_add)).all()
        elif hasattr(user, 'servers_id'):
            user.servers = Server.query.filter(Server.id.in_(user.servers_id)).all()

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
        schema = UserSchema(many=True, exclude=['email', 'company', 'position'])
        query = User.query
        for key, item in request.args.items():
            query = query.filter(getattr(User, key).like(item))
        return paginate(query, schema)

    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)
        print(request.json)
        if not 'company_token' in request.json:
            return {'msg': 'not company'}, 404
        company = Company.query.filter_by(token=request.json['company_token']).first()
        if not company:
            return {'msg': 'not found company'}, 404
        company.users.append(user)
        user.company_id = company.id

        db.session.add(user)
        db.session.commit()

        return {"msg": "user created", "user": schema.dump(user)}, 201
