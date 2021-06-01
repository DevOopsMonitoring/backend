from flask import Flask
from flask_cors import CORS

from src import api
from src import auth
from src.extensions import db
from src.extensions import jwt
from src.extensions import migrate


def create_app(testing=False):
    app = Flask("src")
    app.config.from_object("src.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)
    CORS(app)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['TRAP_HTTP_EXCEPTIONS'] = True

    return app


def configure_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
