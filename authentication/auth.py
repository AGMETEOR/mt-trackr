from flask.views import MethodView
from flask import jsonify, request, abort
import json
# from data import Data
import jwt
import datetime
import os
from functools import wraps



class AuthAPI(MethodView):

    # user login and return token
    def post(self):
        if 'username' in request.json and 'password' in request.json:
            token  = jwt.encode({"user":request.get_json()['username'],
             "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},os.getenv('JWT_SECRET'))
            token = token.decode('UTF-8')
            self.token = token
            return jsonify({"username":request.get_json()['username'],"token":token})

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



