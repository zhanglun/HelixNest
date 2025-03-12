import { request } from "@/helpers/request";

import { Button } from "@heroui/react";
import { useEffect, useState } from "react";

export const CompoundCard = (props: any) => {
  const {
    pubchem_cid,
    canonical_smiles,
    created_at,
    isomeric_smiles,
    iupac_name,
    molecular_formula,
    molecular_weight,
  } = props.data;

  const [img, setImg] = useState("");

  function startAnalysis(cid: number) {
    request
      .post("/compounds/start-analysis", {
        chemical: cid,
      })
      .then(({ data }) => {
        console.log(data);
      });
  }

  useEffect(() => {
    props.data.pubchem_cid &&
      setImg(
        `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${props.data.pubchem_cid}/record/PNG?image_size=320x320`,
      );
  }, [props.data.pubchem_cid]);

  return (
    <div className="flex py-3 border-b-1">
      <img alt={isomeric_smiles} className="object-cover w-[140px]" src={img} />
      <div className="flex-1 flex justify-between">
        <div className="grid grid-cols-[auto_1fr] gap-x-3">
          <div>pubchem_cid:</div>
          <div>{pubchem_cid}</div>
          <div>canonical_smiles:</div>
          <div>{canonical_smiles}</div>
          <div>created_at:</div>
          <div>{created_at}</div>
          <div>isomeric_smiles:</div>
          <div>{isomeric_smiles}</div>
          <div>iupac_name:</div>
          <div>{iupac_name}</div>
          <div>molecular_formula:</div>
          <div>{molecular_formula}</div>
          <div>molecular_weight:</div>
          <div>{molecular_weight}</div>
        </div>
        <div>
          <Button
            color="primary"
            size="sm"
            onPress={() => startAnalysis(pubchem_cid)}
          >
            re analysis
          </Button>
        </div>
      </div>
    </div>
  );
};
