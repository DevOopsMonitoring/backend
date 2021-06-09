from flask import request
from src.api.schemas import OrderSchema
from src.extensions import db


def create_order():
    schema = OrderSchema()
    equipment = schema.load(request.json)

    db.session.add(equipment)
    db.session.commit()

    return {"msg": "Order created", "order": schema.dump(equipment)}, 201
