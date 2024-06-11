from flask import Flask, request, jsonify, g, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from functools import wraps
import logging
from flask_mail import Mail
from flask_migrate import Migrate

from controller import controller_blp
from model import model_blp
from config import config_blp


app = Flask(__name__)


log_level = logging.DEBUG
log_file = "app.log"
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_mode = "a"

logging.basicConfig(
    filename=log_file, filemode=log_mode, format=log_format, level=log_level
)

db = SQLAlchemy(app)
migrate = Migrate(app, db, command='migrate')
mail=Mail(app)


load_dotenv()


with app.app_context():
    # db.drop_all()
    db.create_all()


app.register_blueprint(controller_blp)
app.register_blueprint(model_blp)
app.register_blueprint(config_blp)



if __name__ == "__main__":
    app.run(debug=True)
