from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', [InputRequired(message='Введите имя')])
    address = StringField('Ваш адрес', [InputRequired(message='Введите адрес')])
    email = StringField('Ваш e-mail', [InputRequired(message='Укажите e-mail'), Email()])
    phone = StringField('Ваш номер телефона', [InputRequired(message='Введите номер телефона')])
    submit = SubmitField('Отправить заказ')


class RegistrationForm(FlaskForm):
    mail = StringField('Введите почту', [Email()])
    password = PasswordField('Введите пароль', [Length(min=5)])
    submit = SubmitField('Зарегистрироваться')