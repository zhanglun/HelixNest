import requests
from celery import shared_task
from app.services.pubchem_client import fetch_compound, fetch_pdb_by_inchikey
from app.models.compound import CompoundModel

def pubchem_retry_handler(exc):
    if isinstance(exc, requests.HTTPError):
      raise exc

@shared_task(
  bind=True,
  autoretry_for=(requests.exceptions.RequestException,),
  max_retries=3,
  retry_backoff=30
)
def fetch_pubchem_data(self, chemical_identifier):
  try:
    self.update_state(state='PROGRESS', meta={'progress': 20})

    data = fetch_compound(chemical_identifier)

    return data

  except Exception as e:
    raise e

@shared_task(
  bind=True,
  autoretry_for=(requests.exceptions.RequestException,),
  max_retries=3,
  retry_backoff=30
)
def fetch_pdb_data(self, chemical_identifier):
  try:
    self.update_state(state='PROGRESS', meta={'progress': 20})

    data = fetch_pdb_by_inchikey(chemical_identifier)

    return data

  except Exception as e:
    raise e
