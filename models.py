from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False, unique=True)
    orders = db.relationship('Order', back_populates='client')

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


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