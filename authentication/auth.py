from flask.views import MethodView
from flask import jsonify, request, abort
import json
import bcrypt
# from data import Data
import jwt
import datetime
import os
from functools import wraps
from dbHandler import UserDatabaseHandler

userdb = UserDatabaseHandler("test_db")
userdb.create_table("users_db")



class AuthAPI(MethodView):
    def generate_token(self,user):

        token  = jwt.encode({"user":user,"exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},os.getenv('JWT_SECRET'))
        token = token.decode('UTF-8')
        return token
        
    # user login and return token
    def post(self):
        if 'username' in request.json and 'password' in request.json:
            user = request.get_json()['username']
            self.token = self.generate_token(user)
            return jsonify({"username":request.get_json()['username'],"token":token})
        elif 'username' in request.json and 'password' in request.json and 'status' in request.json:
            username = request.get_json()['username']
            my_user = userdb.get_single_record("users_db",username)
            if my_user != None:

                password = bcrypt.hashpw(request.get_json()['password'], bcrypt.gensalt())
                status = request.get_json()['status']
                created = str(datetime.datetime.utcnow())
                userdb.insert_new_record("users_db",username = username,password=password,type = status, created=created)
                return jsonify({
                    "message":"You were successfully signed up",
                    "login":"http://127.0.0.1:5001/api/v1/login/"}),201
            else:
                return jsonify({"error":"Username already exists!"})
        
        else:
            return jsonify({"error":"Please provide username or password"}),401

    def login_required(f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            if 'Authorization' in request.headers:
                if request.headers['Authorization']:
                    token = request.headers["Authorization"]
                    try:
                        payload = jwt.decode(token, os.getenv("JWT_SECRET"))
                        print(payload['user'])
                        user =  payload['user']
                        
                    except jwt.ExpiredSignatureError:
                        return jsonify({"error":"Signature expired. Please log in again."}),401
                    except jwt.InvalidTokenError:
                        return jsonify({"error":"Invalid token. Please log in again."}),401
                else:
                    return jsonify({"error":"Authentication token was not provided"}),401
            else:
                return jsonify({"error":" Auth Headers not set"})

            return f(user,*args,**kwargs)
        return decorated_function



