from ..middleware.login_required import login_required
from flask import request,jsonify,g
from flask_smorest import Blueprint
from ..model.tags_model import Tag
from ..model.posts_model import Post
from ..db.db import db
from ..schema.post_schema import PostSchema,PostRequestSchema

bp=Blueprint('create_post',__name__)

@bp.post("/create-post")
@login_required
@bp.arguments(PostRequestSchema)
@bp.response(201,PostSchema)
def create_post(data):
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

    return post

    # if post.id:
    #     return jsonify({"message": "Post added Successfully"}), 201
    # else:
    #     return (
    #         jsonify(
    #             {"message": "Post creation failed. Some error occurred on database"}
    #         ),
    #         400,
    #     )

