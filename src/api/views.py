from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from src.api.resources import UserResource, UserList
from src.api.resources import ServerList, ServerResource, generate_new_token
from src.api.resources import CompanyList, CompanyResource
from src.api.resources import PositionList, PositionResource
from src.api.resources import SensorResource, SensorList
from src.api.resources import ReadingRuleResource, ReadingRuleList


blueprint = Blueprint("src", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")

api.add_resource(ServerResource, "/servers/<int:server_id>", endpoint="server_by_id")
api.add_resource(ServerList, '/servers', endpoint='servers')
blueprint.route("/servers/<int:server_id>/refresh", methods=["POST"])(generate_new_token)

api.add_resource(CompanyResource, "/companies/<int:company_id>", endpoint="company_by_id")
api.add_resource(CompanyList, '/companies', endpoint='companies')

api.add_resource(PositionResource, "/positions/<int:position_id>", endpoint="position_by_id")
api.add_resource(PositionList, '/positions', endpoint='positions')

api.add_resource(SensorResource, "/sensors/<int:sensor_id>", endpoint="sensor_by_id")
api.add_resource(SensorList, '/sensors', endpoint='sensors')

api.add_resource(ReadingRuleResource, "/rule/<server_token>", endpoint="reading_rule_by_token")
api.add_resource(ReadingRuleResource, "/rule/<int:rule_id>", endpoint="reading_rule_by_id")
api.add_resource(ReadingRuleList, '/rule', endpoint='reading_rules')


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify({'error': e.messages}), 400
