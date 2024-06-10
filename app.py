from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import bcrypt
import jwt
import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"]='asdfasd'

db = SQLAlchemy(app)

load_dotenv()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile = db.relationship("Profile", uselist=False, back_populates="user")
    posts = db.relationship("Post", backref="user", lazy=True)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    user = db.relationship("User", uselist=False, back_populates="profile")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tags=db.relationship('Tag',secondary='tag_table',lazy='subquery',backref=db.backref('posts',lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)


tag_table=db.Table('tag_table',
    db.Column('post_id',db.Integer,db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'),primary_key=True),
)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route("/")
def home():
    return "Homepage"


@app.post("/create-user")
def create_user():
    try:
        data = request.json
        name = data.get("name")
        bio = data.get("bio")
        email = data.get("email")
        password = data.get("password").encode('utf-8')
        salt=bcrypt.gensalt(rounds=12)
        hash_pass=bcrypt.hashpw(password,salt);

        user = User(name=name,email=email,password=hash_pass)
        profile = Profile(bio=bio)
        user.profile = profile

        db.session.add(user)
        db.session.commit()

        if user.id is not None:
            return jsonify({"message": "User Added Successfully"}), 201
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


@app.get("/users")
def get_users():
    try:
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                "id": user.id,
                "name": user.name,
                "bio": user.profile.bio,
                "post": [],
            }
            for post in user.post:
                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "description": post.description,
                }

                user_data['post'].append(post_data)
            user_list.append(user_data)

        return jsonify({
            "data":user_list
        }), 200
    
    except Exception as err:
        return (
            jsonify({"message": "Operation failed!", "Error": f"The Error is {err}"}),
            500,
        )

@app.post("/create-post")
def create_post():
    data = request.json
    username = data.get("username")
    title = data.get("title")
    description = data.get("description")
    tags_data=data.get("tags",[])

    user = User.query.filter_by(name=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    tags=[]
    for tag_name in tags_data:
        tag=Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag=Tag(name=tag_name)
            db.session.add(tag)
        tags.append(tag)
    
    post = Post(title=title, description=description, user=user, tags=tags)

    db.session.add(post)
    db.session.commit()

    if post.id:
        return jsonify({"message": "Post added Successfully"}), 201
    else:
        return jsonify({"message": "Post creation failed. Some error occurred on database"}), 400




@app.get("/posts")
def get_posts():
    try:
        posts = Post.query.all()
        print(posts)
        post_list = []
        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "user": post.user.name,
                "tags": [tag.name for tag in post.tags]
            }
            post_list.append(post_data)

        return jsonify({"data": post_list}), 200

    except Exception as err:
        return jsonify({"message": "Operation failed!", "Error": f"The Error is {err}"}), 500
    

@app.post('/login')
def login():
    data=request.json
    email=data.get('email')
    password=data.get('password').encode('utf-8')

    user=User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if bcrypt.checkpw(password, user.password):
        token = jwt.encode(
            {
                'user_email':user.email,
                'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=1)
            },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401




if __name__ == "__main__":
    app.run(debug=True)
