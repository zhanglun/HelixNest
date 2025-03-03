from flask import Blueprint, request, jsonify, current_app

views_bp = Blueprint("view", __name__)

@views_bp.route("/")
def index():
  return "Hello World!"

@views_bp.route("/login")
def login():
  return "Login"
