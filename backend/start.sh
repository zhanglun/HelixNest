#!/bin/sh

# 启动 Celery Worker（后台）
celery -A celery_worker.celery worker --loglevel=info &

# 前台运行 Gunicorn（保持容器存活）
exec gunicorn --bind 0.0.0.0:5000 --workers=4 "app:create_app()"
