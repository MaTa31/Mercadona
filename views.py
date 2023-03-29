from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from io import BytesIO
from PIL import Image
import base64

import os

from flask_sqlalchemy.session import Session
from sqlalchemy import create_engine, func, exc

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET_KEY'

username_db = "AdminMercadona"
password_db = "Studi123"
host_db = "localhost"
port_db = "5432"
database_name = "mercadona"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/mercadona"

# = create_engine(f'postgresql://{username_db}:{password_db}@{host_db}:{port_db}/{database_name}')
# session = Session(engine)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Products, Category


@app.route('/')
def get_product():
    products = Products.query.all()
    image_list = []

    for product in products:
        image = base64.b64encode(product.image).decode('ascii')
        image_list.append(image)

    return render_template("home.html", image_list=image_list, products=products)


@app.route('/panel')
def panel():
    categories = Category.query.all()
    products = Products.query.all()

    return render_template('panel.html', products=products, categories=categories)


@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':

        date_promo = request.form['DateFinPromo']
        promo = request.form['promoNumber']
        type_file = request.files.get('image').mimetype

        if date_promo == '':
            date_promo = None
        if promo == '':
            promo = None


        if type_file == 'image/jpg' or type_file == 'image/jpeg' or type_file == 'image/png':

            new_product = Products(name_product=request.form.get('name_product'),
                                   description=request.form.get('description'),
                                   category=request.form.get('category'),
                                   image=request.files.get('image').read(),
                                   price=request.form.get('price'),
                                   date_promo=date_promo,
                                   promo=promo)

            try:
                db.session.add(new_product)
                db.session.commit()
            except exc.SQLAlchemyError:
                flash("Une erreur est survenue veuillez réessayer", 'error')
                return redirect(url_for('panel'))
        else:
            flash("Merci d'utiliser le format JPG JPEG ou PNG pour l'image", 'warning')
            return redirect(url_for('panel'))

        flash('Produit modifier avec succée', 'success')
        return redirect(url_for('panel'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit_product(id):
    product_select = Products.query.get_or_404(id)
    categories = Category.query.all()


    if request.method == 'POST':

        date_promo = request.form['DateFinPromo']
        promo = request.form['promoNumber']
        type_file = request.files.get('image').mimetype

        if date_promo == '':
            date_promo = None
        if promo == '':
            promo = None

        if type_file == 'image/jpg' or type_file == 'image/jpeg' or type_file == 'image/png':

            product_select.name_product = request.form.get('name_product')
            product_select.description = request.form.get('description')
            product_select.category = request.form.get('category')
            product_select.image = request.files.get('image').read()
            product_select.price = request.form.get('price')
            product_select.date_promo = date_promo
            product_select.promo = promo

            try:
                db.session.add(product_select)
                db.session.commit()
            except exc.SQLAlchemyError:
                flash("Une erreur est survenue veuillez réessayer", 'error')
                return redirect(url_for('panel'))

        else:
            flash("Merci d'utiliser le format JPG JPEG ou PNG pour l'image", 'warning')
            return redirect(url_for('panel'))



        flash('Produit ajouté avec succée', 'success')
        return redirect(url_for('panel'))

    return render_template('edit.html', categories=categories, product=product_select)


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_product(id):
    product_select = Products.query.get_or_404(id)
    db.session.delete(product_select)
    db.session.commit()
    flash('Produit supprimer avec succée')
    return redirect(url_for('panel'))


# starting the app

if __name__ == '__main__':
    app.run(debug=True)
