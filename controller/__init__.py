from .create_post_controller import bp as create_post 
from .create_user_controller import bp as create_user
from .custom_error import bp as c_error
from .get_post_controller import bp as get_post
from .get_user_controller import bp as get_user
from .home_controller import bp as home
from .login import bp as signin
from .upload_avatar_controller import bp as upload 


blueprints=[
    create_post,
    create_user,
    c_error,
    get_post,
    get_user,
    home,
    signin,
    upload

]

def register_blueprints(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)