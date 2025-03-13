import requests
from flask import current_app
from requests.exceptions import RequestException
from app.utils.exceptions import RemoteServiceError

def fetch_compound(cid: str) -> dict:
  current_app.logger.info("cid", type(cid))

  url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"

  # 判断是否为CID（纯数字）
  if cid.isdigit():
    url += f"cid/{cid}/JSON"
  else:  # 假定为名称
    url += f"name/{cid}/JSON"

  try:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    pc_data = resp.json()

    result = {
      'pubchem_cid': cid,
      'inchi_key': None,
      'iupac_name': None,
      'molecular_formula': None,
      'molecular_weight': None,
      'canonical_smiles': None,
      'isomeric_smiles': None,
      'other_smiles': []
    }

    for prop in pc_data['PC_Compounds'][0]['props']:
      urn = prop.get('urn', {})
      label = urn.get('label', '').lower()
      name = urn.get('name', '').lower()
      value = prop.get('value', {})

      if 'inchikey' in label or 'inchikey' in name:
        result['inchi_key'] = value.get('sval')

      # 处理IUPAC名称
      if 'iupac name' in label or 'iupac name' in name:
        result['iupac_name'] = value.get('sval')

      # 处理分子式
      elif 'molecular formula' in label:
        if 'sval' in value:
          result['molecular_formula'] = value['sval']
        elif 'ival' in value:  # 异常情况处理
            result['molecular_formula'] = str(value['ival'])

      # 处理分子量
      elif 'molecular weight' in label:
        if 'sval' in value:
          result['molecular_weight'] = value['sval']
        elif 'ival' in value:  # 异常情况处理
            result['molecular_weight'] = str(value['ival'])

      # 处理SMILES（优先顺序：Canonical > Isomeric > 其他）
      elif any(kwd in label + name for kwd in ['smiles']):
        smiles_value = value.get('sval')
        if not smiles_value: continue

        if 'canonical' in label + name:
          if not result['canonical_smiles']:  # 保留第一个遇到的规范式
            result['canonical_smiles'] = smiles_value
        elif 'isomeric' in label + name:
          if not result['isomeric_smiles']:  # 保留第一个遇到的立体式
            result['isomeric_smiles'] = smiles_value
        else:
          result['other_smiles'].append(smiles_value)  # 记录其他类型

    # 降级逻辑：如果未获得规范式，尝试使用其他类型
    if not result['canonical_smiles']:
        result['canonical_smiles'] = result['isomeric_smiles'] \
                                    or (result['other_smiles'][0] if result['other_smiles'] else None)

    return result
  except requests.HTTPError as e:
    raise e
  except RequestException as e:
    current_app.logger.error("cid", type(cid))
    raise RemoteServiceError()


def list_compounds() -> list:
  mongo_client = current_app.extensions["mongo"]
  db = mongo_client[current_app.config["MONGO_DATABASE_NAME"]]

  compounds = db.compounds.find()

  return list(compounds)

def fetch_pdb_by_inchikey(inchikey: str) -> dict:
  url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{inchikey}/pdb/JSON"
  query = {
    "query": {
      "type": "group",
      "logical_operator": "and",
      "nodes": [
        {
          "type": "terminal",
          "service": "text",
          "parameters": {
            "attribute": "rcsb_chem_comp_inchikey",
            "operator": "exact_match",
            "value": inchikey
          }
        }
      ]
    },
    "return_type": "chem_comp"
  }

  try:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()
  except requests.HTTPError as e:
    raise e
  except RequestException as e:
    current_app.logger.error("cid", type(inchikey))
    raise RemoteServiceError()
