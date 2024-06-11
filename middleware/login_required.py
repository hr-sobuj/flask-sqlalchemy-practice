from functools import wraps
from flask import request,jsonify
from app import app 
from model.users import User
import jwt

def login_required(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            g.user = User.query.filter_by(email=data["user_email"]).first()
            if not g.user:
                return jsonify({"message": "User not found"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token is expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return func(*args, **kwargs)

    return inner_func
