from flask import Flask

from .main.routes.routes import * 
from .main.routes.hardware_routes import * 
from .main.routes.paperwork_routes import * 

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'XZas1232ssd'


  app.register_blueprint(main, url_prefix='/')
  app.register_blueprint(hardware, url_prefix='/hardware')
  app.register_blueprint(paperwork, url_prefix='/paperwork')


  return app

