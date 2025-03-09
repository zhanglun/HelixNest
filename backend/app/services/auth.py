import hashlib
import json
from flask import current_app, request, jsonify, session
# from werkzeug.security import check_password_hash
from datetime import datetime
from app.utils.exceptions import InvalidCredentialsError, UserNotActiveError

def const_time_compare(a, b):
  """恒定时间比较防止时序攻击"""
  if len(a) != len(b):
    return False

  result = 0

  for x, y in zip(a, b):
    result |= ord(x) ^ ord(y)

  return result == 0

def login_user(username, password):
  """
  Authenticate a user and generate a JWT token.
  Args:
    username (str): The username of the user attempting to log in
    password (str): The password to verify against stored hash
  Returns:
    tuple: A tuple containing:
      - JSON response with token and user info if successful
      - HTTP status code (200 for success, 401/404 for errors)
  """

  # Get MongoDB client
  mongo_client = current_app.extensions["mongo"]
  db = mongo_client[current_app.config["MONGO_DATABASE_NAME"]]

  # Find user by username
  user = db.users.find_one(
    {"username": username},
  )

  if not user:
    raise InvalidCredentialsError()

  # # 验证密码（带盐值哈希）
  # input_hash = hashlib.sha256(
  #   (password + user['salt']).encode()
  # ).hexdigest()

  # 使用恒定时间比较防止时序攻击
  # if not const_time_compare(password, user['password']):
  #   return jsonify({
  #     "status": "error",
  #     "message": "Invalid credentials"
  #   }), 401

  # Verify password
  # if not check_password_hash(user["password"], password):
  #   return jsonify({"error": "Invalid password"}), 401

  if not user["password"] == password:
    raise InvalidCredentialsError()

  del user["password"]
  user["id"] = str(user["_id"])
  del user["_id"]

  return user

def logout():
  """安全登出"""
  session.clear()  # 服务端立即销毁Session
  return {"status": "Logged out"}


def get_login_user():
    """Get current logged in user's complete information"""
    if not session.get('user_id'):
        return None

    # Get MongoDB client
    mongo_client = current_app.extensions["mongo"]
    db = mongo_client[current_app.config["MONGO_DATABASE_NAME"]]

    # Find user by username
    user = db.users.find_one({"username": session.get('user_id')})

    if user:
        # Remove sensitive information
        if 'password' in user:
            del user['password']
        if 'salt' in user:
            del user['salt']

        return user

    return None
