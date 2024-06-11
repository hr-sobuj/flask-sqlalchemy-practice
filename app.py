from flask import Flask, request, jsonify, g, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import bcrypt
import jwt
import datetime
from functools import wraps
import logging
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = "asdfasd"
app.config["UPLOAD_DIR"] = "uploads"

log_level = logging.DEBUG
log_file = "app.log"
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_mode = "a"

logging.basicConfig(
    filename=log_file, filemode=log_mode, format=log_format, level=log_level
)

db = SQLAlchemy(app)

load_dotenv()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False,unique=True)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
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
    tags = db.relationship(
        "Tag",
        secondary="tag_table",
        lazy="subquery",
        backref=db.backref("posts", lazy=True),
    )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)


tag_table = db.Table(
    "tag_table",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

with app.app_context():
    # db.drop_all()
    db.create_all()


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
        password = data.get("password").encode("utf-8")
        salt = bcrypt.gensalt(rounds=12)
        hash_pass = bcrypt.hashpw(password, salt)

        user = User(name=name, email=email, password=hash_pass)
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

                user_data["post"].append(post_data)
            user_list.append(user_data)

        return jsonify({"data": user_list}), 200

    except Exception as err:
        return (
            jsonify({"message": "Operation failed!", "Error": f"The Error is {err}"}),
            500,
        )


@app.post("/create-post")
@login_required
def create_post():
    data = request.json
    username = data.get("username")
    title = data.get("title")
    description = data.get("description")
    tags_data = data.get("tags", [])

    user = g.user
    tags = []
    for tag_name in tags_data:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        tags.append(tag)

    post = Post(title=title, description=description, user=user, tags=tags)

    db.session.add(post)
    db.session.commit()

    if post.id:
        return jsonify({"message": "Post added Successfully"}), 201
    else:
        return (
            jsonify(
                {"message": "Post creation failed. Some error occurred on database"}
            ),
            400,
        )


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
                "tags": [tag.name for tag in post.tags],
            }
            post_list.append(post_data)

        return jsonify({"data": post_list}), 200

    except Exception as err:
        return (
            jsonify({"message": "Operation failed!", "Error": f"The Error is {err}"}),
            500,
        )


@app.post("/login")
def login():
    data = request.json
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
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@app.patch("/avatar")
@login_required
def upload_avatar():
    try:
        user=g.user
        data=request.files['file']
        file_name=data.filename
        file_split=file_name.split('.')
        file_extention=file_split[len(file_split)-1]
        current_time=datetime.datetime.now()
        file_unique_name = f"{current_time.strftime('%Y%m%d_%H%M%S_%f')}.{file_extention}"


        upload_dir=os.path.join(app.config["UPLOAD_DIR"])
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)

        file_path=os.path.join(upload_dir,file_unique_name)
        data.save(file_path)
        user.avatar=file_path
        db.session.commit()
        return jsonify({
            'message': 'Avatar uploaded successfully!'
        })
    except FileNotFoundError as e:
        return custom_error({"error": "Directory not found", "message": str(e)}, 404)
    except Exception as e:
        return custom_error({"error": "Internal Server Error", "message": str(e)}, 500)


def custom_error(message, status_code): 
    return make_response(jsonify(message), status_code)

@app.errorhandler(Exception)
def handler_exception(e):
    return jsonify({
        "Error":'An error occurred: {}'.format(str(e))
    }),500

@app.get('/error')
def error_raise():
    raise Exception('This is an error')

if __name__ == "__main__":
    app.run(debug=True)
