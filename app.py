from flask import Flask
from dotenv import load_dotenv
from .controller import register_blueprints
from .db.db import db_init
from .others.mailer import mail_init
from .config import app_config
from flask_smorest import Api

app = Flask(__name__)
load_dotenv()


app.config.from_object(app_config.Config)

api=Api(app)

register_blueprints(api)
db_init(app)
mail_init(app)



if __name__ == "__main__":
    app.run(debug=True)
