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

