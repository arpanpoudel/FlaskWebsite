from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mysqldb import MySQL
from sqlalchemy import create_engine

db = SQLAlchemy()
DB_NAME = "database.db"
db_string = "postgresql+psycopg2://bkrosywinjcmur:adb41bdf80128d0add3bb27166c52af7dba9e266a26bfb29e995c0a21287e747@ec2-3-217-146-37.compute-1.amazonaws.com:5432/d3do0ibhcg15e6"
engine = create_engine(db_string)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    mysql = MySQL(app)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'inc0rrect'
    app.config['MYSQL_DB'] = 'final'
    
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()
    

        

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')