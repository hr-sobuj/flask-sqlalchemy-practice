from flask import request,jsonify,current_app
from flask_smorest import Blueprint
from ..model.users import User
import bcrypt,jwt,datetime
from ..schema.user_schema import LoginRequestSchema,LoginResponseSchema

bp=Blueprint('login',__name__)


@bp.post("/login")
@bp.arguments(LoginRequestSchema)
@bp.response(200,LoginResponseSchema)
def login(data):
    email = data.get("email")
    password = data.get("password").encode("utf-8")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if bcrypt.checkpw(password, user.password):
        token = jwt.encode(
            {
                "user_email": user.email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

