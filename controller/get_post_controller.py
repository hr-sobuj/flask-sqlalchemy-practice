from flask import jsonify
from flask_smorest import Blueprint, abort
from ..schema.post_schema import PostSchema

from ..model.posts_model import Post

bp = Blueprint('get_post', __name__)

@bp.get("/posts")
@bp.response(200, PostSchema(many=True))
def get_posts():
    try:
        posts = Post.query.all()
        post_list = []
        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "user": post.user,
                "tags": [tag.name for tag in post.tags],
            }
            post_list.append(post_data)

        return post_list

    except Exception as err:
        abort(500, message="Operation failed!", error=str(err))
