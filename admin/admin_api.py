from flask.views import MethodView
from flask import jsonify, request, abort
import json
from dbHandler import DatabaseHandler, UserDatabaseHandler
import jwt
import os
from authentication.views import AuthAPI
import datetime
import pprint
from flask import current_app as app


class AdminAPI(MethodView):

    @AuthAPI.login_required
    def get(user, self):

        db = DatabaseHandler(app.config['DATABASE_URL'])
        db.create_table("requests_db")
        userdb = UserDatabaseHandler(app.config['DATABASE_URL'])
        userdb.create_table("new_users_db")

        my_user = userdb.get_single_record(user, "new_users_db")

        if my_user[3] != "admin":
            return jsonify({"error": "Access denied"}), 403

        requestItems = db.get_all_records("requests_db")

        items = {"requests": []}
        for i in requestItems:
            _dict = {
                "id": i[0],
                "user": i[1],
                "title": i[2],
                "department": i[3],
                "detail": i[4],
                "status": i[5],
                "created": i[6]
            }
            items['requests'].append(_dict)

        return jsonify(items), 200

    @AuthAPI.login_required
    def put(user, self, requestId, action):

        db = DatabaseHandler(app.config['DATABASE_URL'])
        userdb = UserDatabaseHandler(app.config['DATABASE_URL'])

        my_user = userdb.get_single_record(user, "new_users_db")
        if my_user[3] != "admin":
            return jsonify({"error": "Access denied"}), 403

        actions = ["approve", "disapprove", "resolve"]

        if requestId and action in actions:
            print(requestId)
            print(action)
            requestItem = db.get_single_record("id", requestId, "requests_db")

            username = requestItem[1]
            title = requestItem[2]
            department = requestItem[3]
            detail = requestItem[4]
            status = requestItem[5]
            created = requestItem[6]

            if status == "pending" and action == "approve":
                db.update_record(requestId, "requests_db", username=username, title=title,
                                 department=department, detail=detail, status="approved", created=str(created))
                return jsonify({"message": "Approved"}), 200

            if status == "pending" and action == "disapprove":
                db.update_record(requestId, "requests_db", username=username, title=title,
                                 department=department, detail=detail, status="disapproved", created=str(created))
                return jsonify({"message": "Disapproved"}), 200

            if status == "pending" and action == "resolve":
                db.update_record(requestId, "requests_db", username=username, title=title,
                                 department=department, detail=detail, status="resolved", created=str(created))
                return jsonify({"message": "Resolved"}), 200

            if status == "approved" and action == "approve":
                return jsonify({"message": "Was already approved"}), 200

            if status == "approved" and action == "resolve":
                db.update_record(requestId, "requests_db", username=username, title=title,
                                 department=department, detail=detail, status="resolved", created=str(created))
                return jsonify({"message": "Resolved"}), 200

            if status == "approved" and action == "disapprove":
                db.update_record(requestId, "requests_db", username=username, title=title,
                                 department=department, detail=detail, status="disapproved", created=str(created))
                return jsonify({"message": "Disapproved"}), 200

            if status == "disapproved" and action == "disapprove":
                return jsonify({"message": "Was already disapproved"}), 200

            if status == "disapproved" and action == "approve":
                return jsonify({"message": "Cant approve .Was already disapproved"}), 200

            if status == "disapproved" and action == "resolve":
                return jsonify({"message": "Cant resolve .Was already disapproved"}), 200

            if status == "resolved" and action == "resolve":
                return jsonify({"message": "Was already resolved"}), 200

            if status == "resolved" and action == "disapprove":
                return jsonify({"message": "Was already resolved"}), 200

            if status == "resolved" and action == "approve":
                return jsonify({"message": "Was already resolved"}), 200

        else:
            return jsonify({"error": "Action specified not allowed"}), 401
