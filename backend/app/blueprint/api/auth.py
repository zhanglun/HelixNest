from flask import Blueprint, current_app

auth_bp = Blueprint("auth", __name__, url_prefix="/")

@auth_bp.route('/login', methods=["POST"])
def login():
  return "login"
