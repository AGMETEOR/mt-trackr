from flask import Flask
from settings import app_configuration


def create_app(mode):
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    app.config.from_object(app_configuration[mode])

    app.config['SECRET_KEY'] = "HAHAHA"

    from app.views import requests
    from authentication.views import authentication

    app.register_blueprint(requests)
    app.register_blueprint(authentication)

    return app
