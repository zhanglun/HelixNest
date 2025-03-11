import requests
from bson.objectid import ObjectId
from celery import chain, group, shared_task
from .pubchem_client import fetch_pubchem_data
from .rdkit_processor import calculate_descriptors
from app.models.compound import CompoundModel

@shared_task(
  bind=True,
  autoretry_for=(requests.exceptions.RequestException,),
  max_retries=3,
  retry_backoff=30
)
def fetch_and_analyze_compound(self, cid):
  pipeline = (
    fetch_pubchem_data.s(cid)
    | process_raw_data.s()
    | store_to_mongodb.s()
  )

  return pipeline()

@shared_task()
def process_raw_data(self, raw_data):
  # doc = {
  #   "pubchem_cid": raw_data["pubchem_cid"],
  #   "meta": {
  #     "formula": raw_data.get("molecular_formula"),
  #     "weight": raw_data.get("molecular_weight")
  #   },
  #   "raw_data": raw_data.get("pubchem_data")
  # }
  self.update_state(state='PROGRESS', meta={'progress': 40})

  return raw_data

@shared_task()
def store_to_mongodb(self, data):
  print("data", data)
  cm = CompoundModel();
  doc_id = cm.collection.insert_one(data).inserted_id

  self.update_state(state='PROGRESS', meta={'progress': 60})

  return str(doc_id)



@shared_task()
def post_storage_analysis(self, doc_id):
  cm = CompoundModel()
  doc = cm.collection.find({"_id": ObjectId(doc_id)})

  self.update_state(state='PROGRESS', meta={'progress': 80})
  analysis_result = calculate_descriptors(doc['canonical_smiles'])

  cm.collection.update_one(
    { "_id": ObjectId(doc_id)},
    { "$set": {
      "analysis": analysis_result
    }}
  )
  self.update_state(state='PROGRESS', meta={'progress': 100})

