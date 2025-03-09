from flask import Blueprint, request, session
from app.services.auth import login_user
from app.utils.api_response import format_response, APIResponse

auth_bp = Blueprint("auth", __name__, url_prefix="/")

@auth_bp.route('/login', methods=["POST"])
# @format_response
def login():
  data = request.get_json()

  if not data or 'username' not in data or 'password' not in data:
    return APIResponse.error(
      http_status=400,
      biz_code=40001,
      message="缺少用户名或密码参数"
    )

  # 调用服务层
  user = login_user(
    username=data['username'],
    password=data['password']
  )

  print(user)

  # 设置Session
  session.permanent = True  # 使会话持久化
  session['user_id'] = str(user["_id"])
  session['logged_in'] = True

  return APIResponse.success(
    data=user,
    message="登录成功"
  )



@auth_bp.route('/current_user', methods=["GET"])
def current_user():
  user_id = session.get("user_id")

  return APIResponse.success(
    data={
      "id": user_id
    }
  )
