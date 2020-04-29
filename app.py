from datetime import date

from flask import Flask, render_template, session, request, redirect
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from forms import OrderForm, RegistrationForm
from config import Config
from models import Client, Meal, Category, Order, db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
admin = Admin(app)

admin.add_view(ModelView(Client, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Order, db.session))


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
    form = OrderForm()
    cart = session.get('cart', [])
    cart.append(meal_id)
    session['cart'] = cart
    status = session.get('auth', [])
    return render_template('cart.html', cart=cart_information(session.get('cart', [])), form=form, status=status)

@app.route('/mealremove/<int:meal_id>')
def mealremove(meal_id):
    form = OrderForm()
    cart = session.get('cart', [])
    cart.remove(meal_id)
    session['cart'] = cart
    status = session.get('auth', [])
    return render_template('cart.html', cart=cart_information(session.get('cart', [])), form=form, status=status)

@app.route('/account/', methods=['GET', 'POST'])
def account():
    if session.get('auth', []):
        client_id = session.get('auth', [])
        client_orders = db.session.query(Order).filter(Order.client_id == client_id).all()
        return render_template('account.html', cart=cart_information(session.get('cart', [])),
                               orders=client_orders)
    else:
        return redirect('/register/')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        mail = form.mail.data
        client = db.session.query(Client).filter(Client.mail == mail).first()
        if client:
            if client.password_valid(form.password.data):
                session['auth'] = client.id
                return redirect('/account/')
            else:
                err_msg = 'Не верный пароль вводишь ты'
                return render_template('register.html', form=form, err_msg=err_msg)
        else:
            new_client = Client(mail=mail, password_hash=generate_password_hash(form.password.data))
            db.session.add(new_client)
            db.session.commit()
            session['auth'] = True
            return redirect('/account/')
    elif request.method == 'POST' and not form.validate_on_submit():
        return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)

@app.route('/logout/')
def logout():
    session['auth'] = False
    return redirect('/register/')


@app.route('/ordered/', methods=['GET', 'POST'])
def ordered():
    form = OrderForm()
    if request.method == 'POST' and form.validate_on_submit():
        order_price = (cart_information(session.get('cart', [])))['total_price']
        status = 'Готовится'
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        list_of_meals = []
        all_cart = (cart_information(session.get('cart', [])))
        meals_in_order = all_cart['meals']
        for meal in meals_in_order.values():
            list_of_meals += [meal['title']]
        str_meals = '; '.join(list_of_meals)
        client_id = session.get('auth', False)
        order = Order(date=date.today(), price=order_price, status=status, mail=email, phone=phone, address=address,
                      composition=str_meals, client_id=client_id)
        db.session.add(order)
        db.session.commit()
        return render_template('ordered.html')
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)