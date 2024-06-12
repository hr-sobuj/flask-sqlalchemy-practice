from flask_smorest import Blueprint


bp=Blueprint('home',__name__)


@bp.route("/")
def home():
    return "Homepage"
