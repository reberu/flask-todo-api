import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))


class Config:
    DEBUG = True
    SECRET_KEY = 'fhdsuaiovhreuio4hu'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, '../database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
