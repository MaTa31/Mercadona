from app import db


class Products(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    name_product = db.Column(db.String(50))
    description = db.Column(db.String(500))
    category = db.Column(db.String(50))
    image = db.Column(db.LargeBinary())
    price = db.Column(db.Float())
    date_promo = db.Column(db.DateTime())
    promo = db.Column(db.Integer())

    def __init__(self, product_id, name_product, description, category, image, price, date_promo, promo):
        super().__init__()
        self.id = product_id
        self.category = category
        self.name = name_product
        self.promo = promo
        self.description = description
        self.image = image
        self.price = price
        self.date_promo = date_promo
