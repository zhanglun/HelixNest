from datetime import datetime
import requests
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from celery import shared_task
from .pubchem_client import fetch_pubchem_data, fetch_pdb_data
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
    | fetch_pdb.s()
    | store_to_mongodb.s()
    | post_storage_analysis.s()
  )

  return pipeline()

@shared_task(bind=True)
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

@shared_task(bind=True)
def fetch_pdb(self, data):
  inchi_key = data['inchi_key']

  if inchi_key is not None:
    pdb_data = fetch_pdb_data(inchi_key)
    print("pdb_data ====> ", pdb_data)
    # data['pdb_data'] = pdb_data

  return data


@shared_task(bind=True)
def store_to_mongodb(self, data):
  """
  Store compound data in MongoDB.

  This task stores the provided compound data into the MongoDB collection. It logs the data being stored and updates the task's progress. After the data is inserted, the inserted document's ID is returned as a string.

  Args:
    data (dict): The compound data to be stored in the database.

  Returns:
    str: The ID of the inserted document as a string.
  """

  print("data", data)
  cm = CompoundModel();
  # doc_id = cm.collection.insert_one(data).inserted_id
  if data.get("created_at") is None:
    data["created_at"] = datetime.now()

  data['updated_at'] = datetime.now()

  result = cm.collection.find_one_and_update(
    {"pubchem_cid": data["pubchem_cid"]},
    {"$set":
      {
        "pubchem_cid": data["pubchem_cid"],
        "iupac_name": data["iupac_name"],
        "inchi_key": data["inchi_key"],
        "molecular_formula": data["molecular_formula"],
        "molecular_weight": data["molecular_weight"],
        "canonical_smiles": data["canonical_smiles"],
        "isomeric_smiles": data["isomeric_smiles"],
        "other_smiles": data["other_smiles"],
        "created_at": data["created_at"],
        "updated_at": data["updated_at"]
      }
    },
    upsert=True,
    return_document=ReturnDocument.AFTER
  )

  print("raw_result", result["_id"])

  self.update_state(state='PROGRESS', meta={'progress': 60})

  return str(result["_id"])


@shared_task(bind=True)
def post_storage_analysis(self, doc_id):
  """
  Perform analysis on a compound document after it has been stored in the database.

  Given a document ID, this task will fetch the document from the database, extract the SMILES string from the document, and then use the SMILES string to calculate molecular descriptors. The descriptors will then be stored in the database in the same document.

  The task will update the progress of the task to 80 before starting the analysis and to 100 after the analysis is finished.

  Args:
    doc_id (str): The document ID of the compound to be analyzed.

  Returns:
    None
  """
  cm = CompoundModel()
  doc = cm.collection.find_one({"_id": ObjectId(doc_id)})

  self.update_state(state='PROGRESS', meta={'progress': 80})

  analysis_result = calculate_descriptors(doc['canonical_smiles'])

  cm.collection.update_one(
    { "_id": ObjectId(doc_id)},
    { "$set": {
      "analysis": analysis_result
    }}
  )
  self.update_state(state='PROGRESS', meta={'progress': 100})

