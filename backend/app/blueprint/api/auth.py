from flask import Blueprint, request, current_app
from app.services.auth import login_user
from app.utils.api_response import format_response

auth_bp = Blueprint("auth", __name__, url_prefix="/")

@auth_bp.route('/login', methods=["POST"])
@format_response
def login():
  username = request.json.get('username', '').strip()
  password = request.json.get('password', '').strip()

  result = login_user(username, password)
  print(result)
  return result
