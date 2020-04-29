from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length


class OrderForm(FlaskForm):
    name = StringField('Имя', [InputRequired(message='Введите имя')])
    address = StringField('Адрес', [InputRequired(message='Введите адрес')])
    email = StringField('E-mail', [InputRequired(message='Укажите e-mail'), Email()])
    phone = StringField('Номер телефона', [InputRequired(message='Введите номер телефона')])
    submit = SubmitField('Отправить заказ')


class RegistrationForm(FlaskForm):
    mail = StringField('Введите почту', [Email()])
    password = PasswordField('Введите пароль', [Length(min=5)])
    submit = SubmitField('Зарегистрироваться')