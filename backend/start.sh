#!/bin/sh

# 前台运行 Gunicorn（保持容器存活）
exec gunicorn --bind 0.0.0.0:6000 --workers=4 "app:create_app()"
