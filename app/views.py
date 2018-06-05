from flask import Blueprint

from app.api import RequestsAPI

requests = Blueprint('requests', __name__)


requests_view = RequestsAPI.as_view('requests')

requests.add_url_rule('/api/v1/users/requests/',
                      view_func=requests_view, methods=['POST'])
requests.add_url_rule('/api/v1/users/requests/', view_func=requests_view,
                      methods=['GET'], defaults={"requestId": None})
requests.add_url_rule('/api/v1/users/requests/<string:requestId>/',
                      view_func=requests_view, methods=['GET', 'PUT', ])
