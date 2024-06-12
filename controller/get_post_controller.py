from flask import jsonify,Blueprint
from ..model.posts_model import Post

bp=Blueprint('get_post',__name__)

@bp.get("/posts")
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
