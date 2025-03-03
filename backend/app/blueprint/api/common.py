from flask import Blueprint, current_app

common_bp = Blueprint("common", __name__, url_prefix="/common")

@common_bp.route('/check_mongo')
def check_mongo():
  try:
    mongo_client = current_app.extensions["mongo"]
    db = mongo_client[current_app.config["MONGO_DATABASE_NAME"]]
    collections = db.list_collection_names()
    return f"MongoDB连接正常，现有集合：{collections}"
  except KeyError:
    return "Mongo客户端未挂载到应用扩展"
  except Exception as e:
    return f"MongoDB操作错误: {str(e)}"
