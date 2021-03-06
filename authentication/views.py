from flask import Blueprint

from authentication.auth import AuthAPI

authentication = Blueprint('authentication', __name__)


auth_view = AuthAPI.as_view('authentication')

authentication.add_url_rule('/auth/login/',
                            view_func=auth_view, methods=['POST'])
authentication.add_url_rule(
    '/auth/signup/', view_func=auth_view, methods=['POST'])
