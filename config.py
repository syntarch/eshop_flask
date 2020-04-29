import os


current_path = os.path.dirname(os.path.realpath(__file__))
db_path = "sqlite:///" + current_path + "\\project.db"


class Config():
    DEBUG = True
    SECRET_KEY = 'top_secret_key'
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
