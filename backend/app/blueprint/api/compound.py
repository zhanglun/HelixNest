import re
from flask import Blueprint, request, jsonify, current_app
from celery.result import AsyncResult

import app.services.pubchem_client as pubchem_client
from app.utils.api_response import APIResponse
from app.tasks.compound_tasks import fetch_and_analyze_compound

compound_bp = Blueprint("compound", __name__, url_prefix="/compounds")

@compound_bp.route("", methods=["GET"])
def list():
  """
  Get a list of all compounds in the database.

  Returns:
    APIResponse: a successful response with a list of all compounds.
  """
  list = pubchem_client.list_compounds()

  print(list)

  return APIResponse.success(data={"compounds": list})

@compound_bp.route("/query", methods=["GET"])
def fetch():
  """
  Fetch a compound from the database.

  Returns:
    APIResponse: a successful response with the compound data.
  """

  cid = request.args.get("cid")

  return pubchem_client.fetch_compound(cid)

@compound_bp.route("/start-analysis", methods=["POST"])
def analysis():
  chemical = request.json.get('chemical', '').strip()

  if not chemical:
    return jsonify({'error': 'Missing chemical identifier'}), 400

  # 进一步验证格式（如CID是否为数字）
  if not chemical.isdigit() and not re.match(r'^[a-zA-Z0-9\s-]+$', chemical):
    return jsonify({'error': 'Invalid chemical identifier'}), 400

  # 启动异步任务
  task = fetch_and_analyze_compound.delay(chemical)

  return jsonify({"task_id": task.id}), 202

@compound_bp.get('/task-status/<task_id>')
def get_task_status(task_id):
  task = AsyncResult(task_id)

  return jsonify({
    "task_id": task.id,
    "status": task.status,
    "result": task.result if task.ready() else None
  })


