from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors

def calculate_descriptors(smiles):
  mol = Chem.MolFromSmiles(smiles)

  if not mol:
    print("no mol")
    return None

  # 并行计算多种描述符
  descriptor_map = {
    'smiles': Chem.MolToSmiles(mol),
    'inchi': Chem.MolToInchi(mol),
    'mol_weight': Descriptors.MolWt(mol),
    'tpsa': Descriptors.TPSA(mol),
    'morgan_fp': AllChem.GetMorganFingerprintAsBitVect(mol, 2).ToBitString(),
  }

  return descriptor_map

def compare_structures(pdb_smiles: str, pubchem_smiles: str) -> bool:
    mol1 = Chem.MolFromSmiles(pdb_smiles)
    mol2 = Chem.MolFromSmiles(pubchem_smiles)
    return Chem.CanonicalRankedSmiles([mol1, mol2])[0] == 0
