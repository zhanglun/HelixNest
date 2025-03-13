from app import create_app

app = create_app()  # 确保配置加载

celery = app.extensions["celery"]

