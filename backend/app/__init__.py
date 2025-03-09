import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, current_app
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider
from bson import ObjectId
from datetime import datetime
from .celery_config import celery_init_app
from .extensions import extensions
from .utils.api_response import APIResponse
from .utils.exceptions import DomainException

from app.blueprint.api import api_bp
from app.blueprint.views import views_bp

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(basedir)

class MongoJSONProvider(DefaultJSONProvider):
  def default(self, obj):
    if isinstance(obj, ObjectId):
      return str(obj)

    if isinstance(obj, datetime):
      return obj.isoformat()

    return super().default(obj)

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

  app.json_provider_class = MongoJSONProvider
  app.json = MongoJSONProvider(app)

  @app.errorhandler(Exception)
  def handle_domain_exception(e: Exception):
    if isinstance(e, HTTPException):
      return APIResponse.error(
        http_status=e.code,
        biz_code=f"HTTP_{e.code}",
        message=str(e.description)
      )

    if isinstance(e, DomainException):
      return APIResponse.error(
        http_status=e.http_status,
        biz_code=e.biz_code,
        message=str(e)
      )

    logging.exception("系统未捕获错误")  # 记录详细堆栈

    # 根据环境显示错误详情
    message = "服务器内部错误"
    if current_app.config.get("DEBUG"):
      message = f"{type(e).__name__}: {str(e)}"

    return APIResponse.error(
      http_status=500,
      biz_code="SYSTEM_500",
      message=message
    )

  CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

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
