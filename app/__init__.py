## app/__init__.py ##

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

## Init SQLAlchemy so we can use it later in our models ##
db = SQLAlchemy()

def create_app():
    ## Means that we can use 'FLASK_APP=app' to run our Flask application ##
    app = Flask(__name__)

    ## Configure SQLAlchemy ##
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    ## Blueprint for auth routes in our app ##
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    ## Blueprint for non-auth parts of app ##
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        ## Since the user_id is just the primary key of our user table, use it in the query for the user ##
        return User.query.get(int(user_id))

    return app