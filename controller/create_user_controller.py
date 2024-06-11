from app import app 
from middleware.login_required import login_required
from flask import request,jsonify
from model.users import User
from model.profiles_model import Profile
import bcrypt
from db.db import db
from others.mailer import mail
from flask_mail import Message
from sqlalchemy.exc import SQLAlchemyError

@app.post("/create-user")
def create_user():
    try:
        data = request.json
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
            subject="Welcome Email!"
            message_body=f"Hi {name}! Welcome to our website. And Thanks for registration here."

            msg=Message(subject=subject,sender='habibur.rahman@gigalogy.com',recipients=[user.email])
            msg.body=message_body
            try:
                mail.send(msg)
                return jsonify({"message": "User Added Successfully"}), 201
            except Exception as e:
                return jsonify({"Error": f"User creation failed for {e}"}), 500
            
        else:
            return (
                jsonify(
                    {"message": "User creation failed. Some error occurred on database"}
                ),
                400,
            )
    except SQLAlchemyError as err:
        return (
            jsonify(
                {
                    "message": "User creation failed. Some error occurred on server end.",
                    "Error": f"The error is {err}",
                }
            ),
            500,
        )
