from flask import Flask
from dotenv import load_dotenv
from controller.create_user_controller import user_blp

app = Flask(__name__)
load_dotenv()

app.register_blueprint(user_blp)

if __name__ == "__main__":
    app.run(debug=True)
