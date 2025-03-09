import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from .celery_config import celery_init_app
from .extensions import extensions

from app.blueprint.api import api_bp
from app.blueprint.views import views_bp

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(basedir)

def register_logging(app):
  app.logger.setLevel(logging.INFO)

  log_path = os.path.join(basedir, 'logs')

  if not os.path.exists(log_path):
      os.makedirs(log_path)

  formatter = logging.Formatter('%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s')

  file_handler = RotatingFileHandler(os.path.join(log_path, 'app.log'),
                                      maxBytes=10 * 1024 * 1024, backupCount=10)
  file_handler.setFormatter(formatter)
  file_handler.setLevel(logging.INFO)

  if not app.debug:
    app.logger.addHandler(file_handler)

def create_app(test_confg=None) -> Flask:
  app = Flask(__name__, instance_relative_config=True)

  CORS(app, resources=r'/api/*')

  if os.getenv("FLASK_ENV") == "production":
    app.config.from_pyfile('config.prod.py')
  else:
    app.config.from_pyfile('config.dev.py')  # 替换原来的 from_file

  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  register_blueprint(app)
  register_logging(app)

  # 按需初始化扩展
  with app.app_context():
    _init_extensions(app)

  celery_init_app(app)

  return app

def _init_extensions(app):
  extensions.register_request_hooks(app)
  extensions.init_mongo(app)
  extensions.init_session(app)
  extensions.init_celery(app)

def register_blueprint(app):
  app.register_blueprint(views_bp)
  app.register_blueprint(api_bp)
