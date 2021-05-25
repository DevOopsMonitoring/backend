from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from api.api.resources import UserResource, UserList
from api.api.resources import ServerList, ServerResource
from api.api.resources import CompanyList, CompanyResource


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")

api.add_resource(ServerResource, "/servers/<int:server_id>", endpoint="server_by_id")
api.add_resource(ServerList, '/servers', endpoint='servers')

api.add_resource(CompanyResource, "/companies/<int:company_id>", endpoint="company_by_id")
api.add_resource(CompanyList, '/companies', endpoint='companies')


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
