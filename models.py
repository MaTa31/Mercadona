from views import db, request


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






