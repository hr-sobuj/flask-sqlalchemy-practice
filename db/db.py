from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from ..app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db, command='migrate')

with app.app_context():
    db.create_all()