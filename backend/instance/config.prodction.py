import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://admin:qwer1234@cluster0.qmmfo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME", "helix")

CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND", "mongodb+srv://admin:qwer1234@cluster0.qmmfo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
CELERY_MONGODB_BACKEND_SETTINGS={
  'database': os.getenv("CELERY_DATABASE", "helix"),
  'taskmeta_collection': os.getenv("CELERY_TASKMETA_COLLECTION", "celery_tasks"),
}

SECRET_KEY = os.getenv("SECRET_KEY", "secret helix go go")
SESSION_TYPE = 'redis'
SESSION_REDIS = os.getenv('SESSION_REDIS', 'redis://localhost:6379/2')
SESSION_COOKIE_NAME = '__secure_session'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True    # 仅HTTPS传输
SESSION_COOKIE_SAMESITE = 'Lax' # CSRF防御
PERMANENT_SESSION_LIFETIME = 1800  # 30分钟过期

FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

# MQTT Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_USERNAME = os.getenv('MQTT_USERNAME', '')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', '')
MQTT_KEEPALIVE = int(os.getenv('MQTT_KEEPALIVE', 60))
