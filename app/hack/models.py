from hack import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String(64),index=True)
    password = db.Column(db.String)
    seats_bought = db.relationship('Seat')
    
class Stadium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    match = db.Column(db.String)
    seats = db.relationship('Seat')
    
class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taken = db.Column(db.Boolean, default=False)
    price = db.Column(db.Integer)
    buyer = db.Column(db.Integer, db.ForeignKey('user.id'))
    stadium = db.Column(db.Integer, db.ForeignKey('stadium.id'))



