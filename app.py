from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


app = Flask(__name__)
app.secret_key = 'top_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False, unique=True)
    orders = db.relationship('Order', back_populates='client')


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    price = db.Column(db.Integer)
    description = db.Column(db.String(140))
    picture = db.Column(db.String())
    category = db.relationship('Category', back_populates='meals')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    meals = db.relationship('Meal', back_populates='category')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String())
    price = db.Column(db.Integer)
    status = db.Column(db.String(20))
    mail = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    composition = db.Column(db.String())
    client = db.relationship('Client', back_populates='orders')
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))


db.create_all()

class OrderForm(FlaskForm):
    name = StringField('Ваше имя', InputRequired(message='Заполните поле'))
    address = StringField('Ваш адрес', InputRequired(message='Заполните адрес'))
    email = StringField('Ваш e-mail', InputRequired(message='Введите e-mail'))
    telephone = StringField('Ваш номер телефона', InputRequired(message='Укажите номер телефона'))


def cart_information(list_of_id):
    cart_info = {'meals': {}, 'total_price': 0, 'number_of_meals': 0}
    set_of_id = set(list_of_id)
    if list_of_id:
        for meal_id in set_of_id:
            meal_count = list_of_id.count(meal_id)
            meal = db.session.query(Meal).get(meal_id)
            meal_title = meal.title
            meal_price = meal.price
            cart_info['meals'][meal_id] = {'title': meal_title, 'count': meal_count, 'price': meal_price}
            cart_info['total_price'] += (meal_price * meal_count)
            cart_info['number_of_meals'] += 1
    return cart_info


@app.route('/')
def index():
    number_of_categories = db.session.query(Category).count()
    meals_for_main_page = {}
    for category_id in range(1, number_of_categories+1):
        category = db.session.query(Category).get(category_id)
        category_title = category.title
        meals_for_main_page[category_title] = {}
        meals_in_category = db.session.query(Meal).filter(Meal.category_id == category_id).order_by(func.random()).limit(3)
        selected_meals = meals_in_category.all()
        for meal in selected_meals:
            meals_for_main_page[category_title][meal.id] = {'title': meal.title, 'price': meal.price,
                                                            'description': meal.description, 'picture': meal.picture}
    return render_template('main.html', all_meals=meals_for_main_page, cart=cart_information(session.get('cart', [])))

@app.route('/cart/<int:meal_id>')
def cartf(meal_id):
    cart = session.get('cart', [])
    cart.append(meal_id)
    session['cart'] = cart
    if meal_id == 0:
        session.clear()
    return render_template('cart.html', cart=cart_information(session.get('cart', [])))

@app.route('/account/')
def account():
    return render_template('account.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/logout/')
def logout():
    return render_template('login.html')

@app.route('/ordered/')
def ordered():
    return render_template('ordered.html')


if __name__ == '__main__':
    app.run(debug=True)