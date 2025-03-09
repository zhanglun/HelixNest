from celery import Celery
from redis import Redis
from flask import g
from flask_session import Session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .utils.api_response import generate_request_id

class Extensions:
  """集中管理所有第三方扩展"""

  def __init__(self):
    self.celery = None
    self.mongo = None

  def init_celery(self, app):
    """初始化Celery"""
    self.celery = Celery(app.import_name, broker_url = app.config['CELERY_BROKER_URL'],
      backend = app.config['CELERY_RESULT_BACKEND'],
      task_serializer = 'json',
      result_serializer = 'json',
      accept_content = ['json'],
      timezone="Asia/Shanghai",
      enable_utc = True
    )

    # 确保任务在应用上下文中执行
    class ContextTask(self.celery.Task):
      def __call__(self, *args, **kwargs):
        with app.app_context():
          return self.run(*args, **kwargs)

    self.celery.Task = ContextTask

  def init_mongo(self, app):
    if not app.config.get("MONGO_URI"):
      raise ValueError("MongoDB URI未配置")

    self.mongo = MongoClient(
      app.config["MONGO_URI"],
      server_api=ServerApi('1'),
      connectTimeoutMS=3000,  # 3秒连接超时
      socketTimeoutMS=5000     # 5秒操作超时
    )

    try:
      self.mongo[app.config.get("MONGO_DATABASE_NAME")].command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!", app.config.get("MONGO_DATABASE_NAME"))
      app.extensions["mongo"] = self.mongo
    except Exception as e:
      print(e)

  def init_session(self, app):
    if not app.config.get("SESSION_REDIS"):
      raise ValueError("SESSION_REDIS未配置")

    app.config["SESSION_REDIS"] = Redis.from_url(app.config.get("SESSION_REDIS"))

    Session(app)

  def register_request_hooks(self, app):
    @app.before_request
    def set_request_context():
        """每个请求前生成唯一ID"""
        g.request_id = generate_request_id()

# 单例模式全局访问
extensions = Extensions()
