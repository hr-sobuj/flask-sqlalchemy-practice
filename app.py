from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

db=SQLAlchemy(app)

load_dotenv()

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    profile=db.relationship('Profile',uselist=False,back_populates='user')

class Profile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    bio=db.Column(db.String(200),nullable=False)
    user_id=db.Column(db.Integer,Foreign_Key=('user.id'),unique=True)
    user=db.relationship('User',uselist=False,back_populates='profile')

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return 'Homepage'


if __name__=='__main__':
    app.run(debug=True)