


db = SQLAlchemy(app)
migrate = Migrate(app, db, command='migrate')

with app.app_context():
    db.create_all()