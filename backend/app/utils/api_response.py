from functools import wraps
import uuid
import logging
from datetime import datetime
from flask import jsonify, g
import werkzeug.exceptions as http_errors
from .biz_code import BizCode

class APIResponse:
  @staticmethod
  def generate(
    http_status=200,
    biz_code=BizCode.SUCCESS,
    data=None,
    message=None,
    meta=None
  ):
    """生成标准化响应结构"""
    return jsonify({
      "http_code": http_status,
      "biz_code": biz_code,
      "message": message or BizCode.get_message(biz_code),
      "data": data or None,
      "request_id": g.get("request_id", ""),
      "meta": meta
    }), http_status  # 保持与HTTP状态码一致

  @classmethod
  def success(cls, data=None, message=None, biz_code=BizCode.SUCCESS):
    """成功响应快捷方法"""
    return cls.generate(
      http_status=200,
      biz_code=biz_code,
      data=data,
      message=message
    )

  @classmethod
  def error(cls, http_status, biz_code, message=None):
    """错误响应快捷方法"""
    return cls.generate(
      http_status=http_status,
      biz_code=biz_code,
      message=message
    )

def format_response(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    # 执行视图逻辑
    result = func(*args, **kwargs)

    # 自动识别返回类型
    if isinstance(result, tuple):
      data, code, headers = result + (None, None, None)[len(result):]
      return APIResponse.success(data=data), code, headers
    elif isinstance(result, dict):
      return APIResponse.success(data=result)
    else:
      return APIResponse.success(data={'result': result})
  return wrapper


def generate_request_id():
  return f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex}"
