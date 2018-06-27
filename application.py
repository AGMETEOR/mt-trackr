from flask import Flask
from settings import app_configuration
from flask_cors import CORS


def create_app(mode):
    app = Flask(__name__)

    CORS(app,supports_credentials=True, headers=['Content-Type', 'Authorization'])
    

    app.config.from_pyfile('settings.py')

    app.config.from_object(app_configuration[mode])

    from app.views import requests
    from admin.views import admin_requests
    from authentication.views import authentication

    app.register_blueprint(requests)
    app.register_blueprint(authentication)
    app.register_blueprint(admin_requests)

    return app
