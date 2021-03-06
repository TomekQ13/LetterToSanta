from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from ListDoMikolaja.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_message_category = 'info'
login_manager.login_view='users.login'
mail = Mail()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    bcrypt.init_app(app)
    login_manager.init_app(app)    
    mail.init_app(app)

    from ListDoMikolaja.users.routes import users
    from ListDoMikolaja.letters.routes import letters
    from ListDoMikolaja.friends.routes import friends
    from ListDoMikolaja.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(letters)
    app.register_blueprint(errors)
    app.register_blueprint(friends)

    return app

from ListDoMikolaja.models import User