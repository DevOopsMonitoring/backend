from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from src.api.resources import CompanyList, CompanyResource
from src.api.resources import PositionList, PositionResource
from src.api.resources import ReadingRuleResource, ReadingRuleList
from src.api.resources import SensorResource, SensorList
from src.api.resources import ServerList, ServerResource, generate_new_token, generate_file
from src.api.resources import UserResource, UserList
from src.api.resources import ReadDataResource
from .resources import EquipmentList, EquipmentResource
from .resources import reports
from .resources import create_order


blueprint = Blueprint("src", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")

api.add_resource(ServerResource, "/servers/<int:server_id>", endpoint="server_by_id")
api.add_resource(ServerList, '/servers', endpoint='servers')
blueprint.route("/servers/<int:server_id>/refresh", methods=["POST"])(generate_new_token)
blueprint.route("/servers/<int:server_id>/file", methods=["GET"])(generate_file)

api.add_resource(CompanyResource, "/companies/<int:company_id>", endpoint="company_by_id")
api.add_resource(CompanyList, '/companies', endpoint='companies')

api.add_resource(PositionResource, "/positions/<int:position_id>", endpoint="position_by_id")
api.add_resource(PositionList, '/positions', endpoint='positions')

api.add_resource(SensorResource, "/sensors/<int:sensor_id>", endpoint="sensor_by_id")
api.add_resource(SensorList, '/sensors', endpoint='sensors')

api.add_resource(ReadingRuleResource, "/rule/<server_token>", endpoint="reading_rule_by_token")
api.add_resource(ReadingRuleResource, "/rule/<int:rule_id>", endpoint="reading_rule_by_id")
api.add_resource(ReadingRuleList, '/rule', endpoint='reading_rules')

api.add_resource(ReadDataResource, "/data/<int:server_id>", endpoint="read_data_by_id")
api.add_resource(ReadDataResource, "/data/<server_token>", endpoint="read_data_by_token")

api.add_resource(EquipmentResource, "/equipments/<int:equipment_id>", endpoint="equipments_by_id")
api.add_resource(EquipmentList, "/equipments", endpoint="equipments")

blueprint.route("/reports/number_employees_in_companies", methods=["GET"])(reports.number_employees_in_companies)
blueprint.route("/reports/number_employees_in_companies/print", methods=["GET"])(reports.number_employees_in_companies_print)

blueprint.route("/reports/number_servers_in_companies", methods=["GET"])(reports.number_servers_in_companies)
blueprint.route("/reports/number_servers_in_companies/print", methods=["GET"])(reports.number_servers_in_companies_print)

blueprint.route("/reports/count_sensors_on_server", methods=["GET"])(reports.count_sensors_on_server)
blueprint.route("/reports/count_sensors_on_server/print", methods=["GET"])(reports.count_sensors_on_server_print)

blueprint.route("/reports/count_fail_on_server/print", methods=["GET"])(reports.count_fail_on_server)

blueprint.route("/order/create", methods=["POST"])(create_order)

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify({'error': e.messages}), 400
