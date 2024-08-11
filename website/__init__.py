from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Creation of database
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    # Maintains integrity and confidentiality of session data
    app.config['SECRET_KEY'] = 'nf hjnfd dlfpsd mgjwo'
    # Connect to DB
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Registers blueprints from other files
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Brings unauthenticated users to login route
    login_manager.init_app(app) # Connects login manager to app

    @login_manager.user_loader # Finds a user based on ID
    def load_user(id):
        return User.query.get(int(id))

    return app

# Creates a DB if not created yet.
def create_database(app):
    if not path.exists('website/' + DB_NAME): # Checks for DB existence
        with app.app_context():
            db.create_all() # Creates db tables if not existing
        print('Created Database!')