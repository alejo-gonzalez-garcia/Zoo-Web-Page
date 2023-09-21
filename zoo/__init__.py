from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from .insertion import insert_data

import sys
sys.dont_write_bytecode = True

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = b""

    # Configure SQLAlchemy
    user = ""
    password = ""
    host = ""
    database = "Zoo"

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://{user}:{password}@{host}/{database}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init the DB
    db.init_app(app)

    # Configure mail
    app.config["MAIL_SERVER"] = '.gmail.com'
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = '@gmail.com'
    app.config["MAIL_DEFAULT_SENDER"] = '@gmail.com'
    app.config["MAIL_PASSWORD"] = ''

    # Init the mail client
    mail.init_app(app)

    # Configure LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from . import model
    @login_manager.user_loader
    def user_loader(email):
        return model.User.query.get(email)

    # Configure blueprints
    from . import main
    from . import auth
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    # Create all the models inside the DB
    db.drop_all(app=app)
    db.create_all(app=app)

    insert_data(model, app)

    return app

