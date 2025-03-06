from flask import Blueprint
from . import common, compound, auth
from flask_cors import CORS

api_bp = Blueprint("api", __name__, url_prefix="/api")

CORS(api_bp, supports_credentials=True)

api_bp.register_blueprint(common.common_bp)
api_bp.register_blueprint(auth.auth_bp)
api_bp.register_blueprint(compound.compound_bp)
