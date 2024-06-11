from flask import Flask
from dotenv import load_dotenv
from controller import controller_blp
from model import model_blp
from config import config_blp
from db import db_blp
from others import other_blp


app = Flask(__name__)
load_dotenv()

app.register_blueprint(controller_blp)
app.register_blueprint(model_blp)
app.register_blueprint(config_blp)
app.register_blueprint(db_blp)
app.register_blueprint(other_blp)

if __name__ == "__main__":
    app.run(debug=True)
