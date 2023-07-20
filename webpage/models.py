from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from webpage import DB_NAME
from flask_login import login_user, login_required, logout_user, current_user


class Watches(db.Model):
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    watch_mid = db.Column(db.String(20), unique=True, nullable=False)
    watch_name = db.Column(db.String(150), nullable=False)
    watch_type = db.Column (db.String(10), nullable=True)
    watch_price= db.Column (db.Integer, nullable=False)
    img_name=db.Column(db.String(50),nullable=False)
    img= db.Column(db.LargeBinary, nullable=False)
    orders = db.relationship('Orders',lazy=True)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime(timezone=True), default=func.now())
    order_count = db.Column(db.Integer, nullable=False )
    email = db.Column(db.String(100), db.ForeignKey('user.email'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    orders = db.relationship('Orders',lazy=True)