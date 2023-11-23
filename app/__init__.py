from flask import Flask
import os


def create_app(config_type=None):
    app = Flask(__name__)

    if config_type == None:
        config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")

    app.config.from_object(config_type)
    register_blueprints(app)

    return app


def register_blueprints(app):
    from .auth import auth

    app.register_blueprint(auth, url_prefix="/")
