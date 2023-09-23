import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    SECRET_KEY = '049c85b801fc4ae13dc9c309fd9dc646e869b40c'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'nichego.db')
    DEBUG = True
    UPLOAD_FOLDER = '/appl/static/uplouds'




