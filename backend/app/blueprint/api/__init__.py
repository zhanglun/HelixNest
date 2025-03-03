from flask import Blueprint
from . import common, compound

api_bp = Blueprint("api", __name__, url_prefix="/api")

api_bp.register_blueprint(common.common_bp)
api_bp.register_blueprint(compound.compound_bp)
