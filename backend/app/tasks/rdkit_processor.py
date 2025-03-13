from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors

def calculate_descriptors(smiles):
  mol = Chem.MolFromSmiles(smiles)

  if not mol:
    print("no mol")
    return None

  # 并行计算多种描述符
  descriptor_map = {
    'mol_weight': Descriptors.MolWt(mol),
    'tpsa': Descriptors.TPSA(mol),
    'morgan_fp': AllChem.GetMorganFingerprintAsBitVect(mol, 2).ToBitString(),
    # "fps": Chem.RDKFingerprint(mol)
  }

  return descriptor_map
