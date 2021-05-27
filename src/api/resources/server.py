from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from src.api.schemas import ServerSchema
from src.models import Server
from src.extensions import db
from src.commons.pagination import paginate


class ServerResource(Resource):
    method_decorators = [jwt_required()]

    def get(self, server_id):
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


@jwt_required()
def generate_new_token(server_id):
    server = Server.query.get_or_404(server_id)
    server.refresh_token()
    db.session.commit()
    schema = ServerSchema()
    return {"server": schema.dump(server)}
