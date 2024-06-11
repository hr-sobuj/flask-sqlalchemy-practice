@app.get("/users")
def get_users():
    # cached_user=redis_store.get('users')
    # if cached_user:
    #     return cached_user
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

        response= jsonify({"data": user_list})
        redis_store.set('users',response,ex=3600)
        return response,200

    except Exception as err:
        return (
            jsonify({"message": "Operation failed!", "Error": f"The Error is {err}"}),
            500,
        )
