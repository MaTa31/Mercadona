from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://FlaskApp:Studi@localhost:5432/mercadona'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Products


@app.route('/')
def home():
    products = Products.query.all()
    return render_template("index.html", products=products)


if __name__ == '__main__':
    app.run()
