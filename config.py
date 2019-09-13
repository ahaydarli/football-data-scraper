import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://doadmin:z9ydmc15oc1c91b1@db-postgresql-fra1-41641-do-user-6517766-0.db.ondigitalocean.com:25060/defaultdb?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
