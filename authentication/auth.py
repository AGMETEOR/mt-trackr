from flask.views import MethodView
from flask import jsonify, request, abort
import json
import bcrypt
import jwt
import datetime
import os
from functools import wraps
from dbHandler import UserDatabaseHandler

userdb = UserDatabaseHandler("test_db")
# userdb.create_table("new_users_db")


class AuthAPI(MethodView):

    def generate_token(self, user):

        token = jwt.encode({"user": user, "exp": datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=60)}, os.getenv('JWT_SECRET'))
        token = token.decode('UTF-8')
        return token

    # user login and return token
    def post(self):
        if 'username' in request.json and 'password' in request.json and 'status' not in request.json:
            user = request.get_json()['username']
            password = request.get_json()['password']
            my_user = userdb.get_single_record(user, "new_users_db")
            if my_user is not None:
                hashed_password = my_user[2]
                if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                    token = self.generate_token(user)
                    return jsonify({"username": user, "token": token})
                else:
                    return jsonify({"error": "Password and username didn't match"})
            else:
                return jsonify({"error": "Wrong username or password"})
        elif 'username' in request.json and 'password' in request.json and 'status' in request.json:

            user = request.get_json()['username']
            my_user = userdb.get_single_record(user, "new_users_db")
            if my_user is None:

                hashed_passw = bcrypt.hashpw(
                    request.get_json()["password"].encode(), bcrypt.gensalt())
                passw = hashed_passw.decode()
                stat = request.get_json()['status']
                cretd = str(datetime.datetime.utcnow())

                userdb.insert_new_record(
                    "new_users_db", username=user, password=passw, type=stat, created=cretd)

                return jsonify({
                    "message": "You were successfully signed up",
                    "login": "http://127.0.0.1:5001/api/v1/login/"}), 201
            elif my_user is not None:
                return jsonify({"error": "Username already exists!"})

        else:
            return jsonify({"error": "Please provide username or password"}), 401

    @staticmethod
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'Authorization' in request.headers:
                if request.headers['Authorization']:
                    token = request.headers["Authorization"]
                    try:
                        payload = jwt.decode(token, os.getenv("JWT_SECRET"))
                        print(payload['user'])
                        user = payload['user']

                    except jwt.ExpiredSignatureError:
                        return jsonify({"error": "Signature expired. Please log in again."}), 401
                    except jwt.InvalidTokenError:
                        return jsonify({"error": "Invalid token. Please log in again."}), 401
                else:
                    return jsonify({"error": "Authentication token was not provided"}), 401
            else:
                return jsonify({"error": " Auth Headers not set"})

            return f(user, *args, **kwargs)
        return decorated_function
