import os

MONGO_URI = "mongodb+srv://admin:qwer1234@cluster0.qmmfo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DATABASE_NAME = "helix"

CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND")

SECRET_KEY = "secret helix go go"
SESSION_TYPE = 'redis'
SESSION_REDIS = os.getenv('SESSION_REDIS')
SESSION_COOKIE_NAME = '__secure_session'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True    # 仅HTTPS传输
SESSION_COOKIE_SAMESITE = 'Lax' # CSRF防御
PERMANENT_SESSION_LIFETIME = 1800  # 30分钟过期

FLASK_PORT = 6000
