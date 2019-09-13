from flask import Flask, session, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

SESSION_TYPE = 'redis'

from app import routes, models, methods
from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSON_SORT_KEYS'] = False


if __name__ == '__main__':
    app.run(debug=True)
