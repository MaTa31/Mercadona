from app import db
from sqlalchemy.dialects.postgresql import JSON


class Products(db.Model):
    __tablename__ = 'Produits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    image = db.Column(db.blob())
    price = db.Column(db.decimal())
    promoDate = db.Column(db.Date())
    promo = db.Column(db.Integer())

    def __init__(self, name, description, image, price, promodate, promo):
        super().__init__()
        self.name = name
        self.promo = promo
        self.description = description
        self.image = image
        self.price = price
        self.promoDate = promodate


