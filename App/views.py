from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_migrate import Migrate
from datetime import date
from werkzeug.security import check_password_hash
import os
import base64



# a optimiser dans un __init__.py
# a optimiser dans un __init__.py
# a optimiser dans un __init__.py
# a optimiser dans un __init__.py

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



# password = generate_password_hash ('Sax89thj@er8', method='sha256')
# print(password)


# a optimiser dans un __init__.py
# a optimiser dans un __init__.py
# a optimiser dans un __init__.py
# a optimiser dans un __init__.py

from App.models import Products, Category, User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    today_date = date.today()

    for product in products:
        image = base64.b64encode(product.image).decode('ascii')
        image_list.append(image)

        if product.promo is None:
            final_price = product.price
        else:
            final_price = round(product.price * ((100 - product.promo) / 100), 2)

    return render_template("home.html", final_price=final_price, image_list=image_list, products=products
                           , today_date=today_date)


@app.route('/<category>', methods=['GET'])
def get_product_by_category(category):
    if Products.query.filter_by(category=category).first() is not None:

        products = Products.query.filter_by(category=category).all()
        image_list = []
        final_price = 0
        today_date = date.today()

        for product in products:
            image = base64.b64encode(product.image).decode('ascii')
            image_list.append(image)

            if product.promo is None:
                final_price = product.price
            else:
                final_price = round(product.price * ((100 - product.promo) / 100), 2)
    else:

        return render_template('missing.html', category=category)

    return render_template("home.html", final_price=final_price, image_list=image_list, products=products,
                           today_date=today_date)


@app.route('/panel', methods=['GET'])
@login_required
def panel():
    categories = Category.query.all()
    products = Products.query.all()

    return render_template('panel.html', products=products, categories=categories)


@app.route('/add_product', methods=['POST'])
@login_required
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

        flash('Produit ajouté avec succée', 'success')
        return redirect(url_for('panel'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
@login_required
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

        flash('Produit modifié avec succée', 'success')
        return redirect(url_for('panel'))

    return render_template('edit.html', categories=categories, products=product_select)


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
@login_required
def delete_product(id):
    product_select = Products.query.get_or_404(id)
    db.session.delete(product_select)
    db.session.commit()
    flash('Produit supprimer avec succée', 'success')
    return redirect(url_for('panel'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_page = True
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Merci de verifier vos identifiants', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        return redirect(url_for('panel'))

    return render_template('login.html', login_page=login_page)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
