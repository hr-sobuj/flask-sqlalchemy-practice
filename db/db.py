from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def db_init(app):
    db.init_app(app)
    migrate.init_app(app, db, command='migrate')

    with app.app_context():
        db.create_all()

    return db, migrate