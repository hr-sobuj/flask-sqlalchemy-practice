from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db = SQLAlchemy(app)

load_dotenv()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    profile = db.relationship("Profile", uselist=False, back_populates="user")


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    user = db.relationship("User", uselist=False, back_populates="profile")


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Homepage"

@app.post('/create-user')
def create_user():
    try:
        data=request.json
        name=data.get('name')
        bio=data.get('bio')

        user=User(name=name)
        profile=Profile(bio=bio)
        user.profile=profile

        db.session.add(user)
        db.session.commit()

        if user.id is not None:
            return jsonify({
                'message':'User Added Successfully'
            }), 201
        else:
             return jsonify({
                'message':'User creation failed. Some error occurred on database'
            }), 400
    except SQLAlchemyError as err:
        return jsonify({
                'message':'User creation failed. Some error occurred on server end.'
            }), 500

@app.get('/users')
def get_users():
    try:
        users=User.query.all()
        user_list=[]
        for user in users:
            user_list.append({
                'id':user.id,
                'name':user.name,
                'bio':user.profile.bio
            })
        return jsonify(user_list), 200
    except Exception as err:
        return jsonify({
            'message':'Operation failed!',
            'Error':f"The Error is {err}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
