from flask import Flask

from .main.routes import *

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'XZas1232ssd'


  app.register_blueprint(main, url_prefix='/')


  return app

