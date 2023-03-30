from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_migrate import Migrate
import os
import base64

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from App.models import Products, Category

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', iserror=True), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', iserror=True), 500


@app.route('/')
def get_product():
    products = Products.query.all()
    image_list = []
    final_price = 0

    for product in products:
        image = base64.b64encode(product.image).decode('ascii')
        image_list.append(image)

        if product.promo is None:
            final_price = product.price
        else:
            final_price = round(product.price * ((100 - product.promo)/100), 2)

    return render_template("home.html", final_price=final_price, image_list=image_list, products=products)


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

    return render_template('edit.html', categories=categories, products=product_select)


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_product(id):
    product_select = Products.query.get_or_404(id)
    db.session.delete(product_select)
    db.session.commit()
    flash('Produit supprimer avec succée')
    return redirect(url_for('panel'))

# starting the app
