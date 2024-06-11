class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False,unique=True)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    profile = db.relationship("Profile", uselist=False, back_populates="user")
    posts = db.relationship("Post", backref="user", lazy=True)
