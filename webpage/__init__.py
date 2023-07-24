import base64
from os import path
import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_wtf.csrf import CSRFProtect
import stripe

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db= SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
DB_NAME = "database.db"
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app=Flask(__name__)
    csrf.init_app(app)

    @app.template_filter('b64encode')
    def base64_encode(value):
        if isinstance(value, str):
           value = value.encode('utf-8')
        encoded_bytes = base64.b64encode(value)
        encoded_str = encoded_bytes.decode('utf-8')
        return encoded_str
    
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%Y-%m-%d %H:%M'):
      return value.strftime(format)
    
    app.config['SECRET_KEY']='tetsinshajshkks'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER']=r"static\uploads"
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    create_database(app)

    login_manager=LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
       from .models import User
       return User.query.get(int(id))
    

    return app

def create_database(app):
    if not path.exists('website/'+ DB_NAME):
        with app.app_context():
           db.create_all()
           print ('Created Database!')