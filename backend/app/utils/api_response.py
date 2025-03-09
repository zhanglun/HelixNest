from functools import wraps
from flask import jsonify, g
import werkzeug.exceptions as http_errors

import uuid
from datetime import datetime


class APIResponse:
  @staticmethod
  def success(data=None, message="success", meta=None, code=200):
    return jsonify({
      "code": code,
      "message": message,
      "data": data or {},
      "request_id": g.request_id,
      "meta": meta
    })

  @staticmethod
  def error(message="error", code=500, details=None):
    return jsonify({
      "code": code,
      "message": message,
      "details": details,
      "request_id": g.request_id,
    }), 500

def format_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # 执行视图逻辑
            result = func(*args, **kwargs)

            print("result", result)

            # 自动识别返回类型
            if isinstance(result, tuple):
                data, code, headers = result + (None, None, None)[len(result):]
                return APIResponse.success(data=data, code=code), code, headers
            elif isinstance(result, dict):
                return APIResponse.success(data=result)
            else:
                return APIResponse.success(data={'result': result})

        except http_errors.HTTPException as e:
            return APIResponse.error(message=e.description, code=e.code)
        except Exception as e:
            # 记录错误日志
            return APIResponse.error(message=str(e), code=500)
    return wrapper


def generate_request_id():
    return f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex}"
