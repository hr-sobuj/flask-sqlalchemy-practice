from flask import request, jsonify
from flask_smorest import Blueprint, abort
from ..model.users import User
from ..model.profiles_model import Profile
import bcrypt
from ..db.db import db
from ..others.mailer import mail
from flask_mail import Message
from sqlalchemy.exc import SQLAlchemyError
from ..schema.user_schema import CreateUserRequestSchema, CreateUserResponseSchema

bp = Blueprint('create_user_with_schema', __name__, description="Operations on user creation with schema")

@bp.route("/create-user-schema", methods=["POST"])
@bp.arguments(CreateUserRequestSchema)
@bp.response(201, CreateUserResponseSchema)
def create_user(data):
    try:
        name = data.get("name")
        bio = data.get("bio")
        email = data.get("email")
        password = data.get("password").encode("utf-8")
        salt = bcrypt.gensalt(rounds=12)
        hash_pass = bcrypt.hashpw(password, salt)

        user = User(name=name, email=email, password=hash_pass)
        profile = Profile(bio=bio)
        user.profile = profile

        db.session.add(user)
        db.session.commit()

        if user.id is not None:
            subject = "Welcome Email!"
            message_body = f"Hi {name}! Welcome to our website. And Thanks for registration here."

            msg = Message(subject=subject, sender='habibur.rahman@gigalogy.com', recipients=[user.email])
            msg.body = message_body
            try:
                mail.send(msg)
                return {"message": "User Added Successfully", "user": user}
            except Exception as e:
                abort(500, message=f"User creation failed for {e}")
        else:
            abort(400, message="User creation failed. Some error occurred on database")
    except SQLAlchemyError as err:
        abort(500, message=f"User creation failed. Some error occurred on server end. Error: {err}")
