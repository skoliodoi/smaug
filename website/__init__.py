import os
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from .models import User
from .main.routes.routes import * 
from .main.routes.hardware_routes import * 
from .main.routes.paperwork_routes import * 
from .main.routes.auth import auth

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = f"{os.environ['FLASK_KEY']}"
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    logged_user = User(user_id)
    return logged_user

  app.register_blueprint(main, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(hardware, url_prefix='/hardware')
  app.register_blueprint(paperwork, url_prefix='/paperwork')


  return app

