from flask import Flask

from api import api
from api import auth
from api.extensions import db
from api.extensions import jwt
from api.extensions import migrate


def create_app(testing=False):
    app = Flask("api")
    app.config.from_object("api.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
