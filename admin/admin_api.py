from flask.views import MethodView
from flask import jsonify, request, abort
import json
from dbHandler import DatabaseHandler, UserDatabaseHandler
import jwt
import os
from authentication.views import AuthAPI
import datetime
import pprint

db = DatabaseHandler("test_db")
# db.create_table("requests_db")
userdb = UserDatabaseHandler("test_db")

class AdminAPI(MethodView):


    @AuthAPI.login_required
    def get(user, self):
        my_user = userdb.get_single_record(user,"new_users_db")
        if my_user[3] != "admin":
            return jsonify({"error":"Access denied"}),403
        

        requestItems = db.get_all_records("requests_db")

        items = {"requests":[]}
        for i in requestItems:
            _dict = {
                "id":i[0],
                "user":i[1],
                "title":i[2],
                "department":i[3],
                "detail":i[4],
                "status":i[5],
                "created":i[6]
            }     
            items['requests'].append(_dict)
        
        return jsonify(items), 200



    

    @AuthAPI.login_required
    def put(user, self, requestId, action):

        my_user = userdb.get_single_record(user,"new_users_db")
        if my_user[3] != "admin":
            return jsonify({"error":"Access denied"}),403

        

        if requestId and action:
            print(requestId)
            print(action)
            requestItem = db.get_single_record("id", requestId, "requests_db")
            db.get_single_record("id",3,"requests_db")

            username = requestItem[1]
            title =requestItem[2]
            department = requestItem[3]
            detail = requestItem[4]
            status = requestItem[5]
            created = requestItem[6]

            if status == "pending":
                db.update_record(requestId,"requests_db",username=username, title= title, department=department, detail=detail,status = "approved",created=str(created))
                return jsonify({"success":"Approved!"}),200
            else:
                return jsonify({"error":"This request is no longer pending and does not need approval"})



