from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from api.api.schemas import ServerSchema
from api.models import Server
from api.extensions import db
from api.commons.pagination import paginate


class ServerResource(Resource):
    method_decorators = [jwt_required()]

    def get(self, server_id):
        print(server_id)
        schema = ServerSchema()
        user = Server.query.get_or_404(server_id)
        return {"server": schema.dump(user)}

    def put(self, server_id):
        schema = ServerSchema(partial=True)
        server = Server.query.get_or_404(server_id)
        server = schema.load(request.json, instance=server)

        db.session.commit()

        return {"msg": "server updated", "server": schema.dump(server)}

    def delete(self, server_id):
        user = Server.query.get_or_404(server_id)
        db.session.delete(user)
        db.session.commit()

        return {"msg": "Server deleted"}


class ServerList(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        schema = ServerSchema(many=True, exclude=['token'])
        query = Server.query
        for key, item in request.args.items():
            query = query.filter(getattr(Server, key).like(item))
        return paginate(query, schema)

    def post(self):
        schema = ServerSchema()
        server = schema.load(request.json)

        db.session.add(server)
        db.session.commit()

        return {"msg": "server created", "server": schema.dump(server)}, 201
