from flask_login import UserMixin
from App.views import db


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name_product = db.Column(db.String(50))
    description = db.Column(db.String(500))
    category = db.Column(db.String(50))
    image = db.Column(db.LargeBinary)
    price = db.Column(db.Float())
    date_promo = db.Column(db.DateTime(), nullable=True)
    promo = db.Column(db.Float())


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name_category = db.Column(db.String(50))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))



