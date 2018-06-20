from flask.views import MethodView
from flask import jsonify, request, abort
import json
from dbHandler import DatabaseHandler
import jwt
import os
from authentication.views import AuthAPI
import datetime
from flask import current_app as app


class RequestsAPI(MethodView):

    # post request
    @AuthAPI.login_required
    def post(user, self):

        db = DatabaseHandler(app.config['DATABASE_URL'])
        db.create_table("requests_db")

        returnObj = {}

        if not request.json:
            abort(400)

        username = user
        title = request.json['title']
        department = request.json['department']
        detail = request.json['detail']
        status = request.json['status']
        created = str(datetime.datetime.utcnow())

        dataR = db.insert_new_record("requests_db", username=username, title=title,
                                     department=department, detail=detail, status=status, created=created)

        returnObj["id"] = dataR[0]
        returnObj["user"] = dataR[1]
        returnObj["title"] = dataR[2]
        returnObj["department"] = dataR[3]
        returnObj["detail"] = dataR[4]
        returnObj["status"] = dataR[5]
        returnObj["created"] = dataR[6]

        return jsonify(returnObj), 201

    @AuthAPI.login_required
    def get(user, self, requestId):
        db = DatabaseHandler(app.config['DATABASE_URL'])
        db.create_table("requests_db")

        returnObj = {}
        if requestId:
            dataR = db.get_single_record("id", requestId, "requests_db", user)

            if dataR is None:
                return jsonify({"error": "Couldn't find request in your data"}), 404

            returnObj["id"] = dataR[0]
            returnObj["user"] = dataR[1]
            returnObj["title"] = dataR[2]
            returnObj["department"] = dataR[3]
            returnObj["detail"] = dataR[4]
            returnObj["status"] = dataR[5]
            returnObj["created"] = dataR[6]

            return jsonify({"requests": [returnObj]}), 200
        else:
            items = {"requests": []}

            requestItems = db.get_all_records("requests_db", user)

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
    def put(user, self, requestId):
        db = DatabaseHandler(app.config['DATABASE_URL'])
        db.create_table("requests_db")
        
        returnObj = {}

        if not request.json:
            abort(400)

        if requestId:
            dataR = db.get_single_record("id", requestId, "requests_db", user)

            username = user
            title = request.json['title']
            department = request.json['department']
            detail = request.json['detail']
            status = dataR[5]
            created = str(datetime.datetime.utcnow())

            if status == "approved":
                return jsonify({"message": "Cannot edit was already approved"})
            else:

                dataR = db.update_record(requestId, "requests_db", username=username, title=title,
                                         department=department, detail=detail, status=status, created=created)
                if dataR:
                    returnObj["id"] = dataR[0]
                    returnObj["user"] = dataR[1]
                    returnObj["title"] = dataR[2]
                    returnObj["department"] = dataR[3]
                    returnObj["detail"] = dataR[4]
                    returnObj["status"] = dataR[5]
                    returnObj["created"] = dataR[6]

                    return jsonify(returnObj), 201
                else:
                    jsonify({"error": "Couldn't update"})
        return jsonify({"error": "ID was not provided"})
