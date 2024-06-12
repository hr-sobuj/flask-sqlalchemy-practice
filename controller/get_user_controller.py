from flask import jsonify
from flask_smorest import Blueprint, abort
from ..schema.user_schema import UserSchema


from ..model.users import User

bp = Blueprint("get_user", __name__)


@bp.get("/users")
@bp.response(200,UserSchema(many=True))
def get_users():
    try:
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                "id": user.id,
                "name": user.name,
                "bio": user.profile.bio if user.profile else None,
                "posts": [],
            }
            for post in user.posts:
                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "description": post.description,
                }

                user_data["posts"].append(post_data)
            user_list.append(user_data)

        return user_list

    except Exception as err:
        abort(500, message="Operation failed!", Error=f"The Error is {err}")
