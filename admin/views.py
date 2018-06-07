from flask import Blueprint

from admin.admin_api import AdminAPI

admin_requests = Blueprint('admin_requests', __name__)


admin_requests_view = AdminAPI.as_view('admin_requests')

admin_requests.add_url_rule('/requests/', view_func=admin_requests_view,
                      methods=['GET'])

admin_requests.add_url_rule('/requests/',view_func=admin_requests_view, methods=['PUT',],defaults={"requestId": None,"action":None})
admin_requests.add_url_rule('/requests/<string:requestId>/<string:action>/',view_func=admin_requests_view, methods=['PUT',])


