import os
import sys

import numpy as np

import pandas as pd
from Bio.PDB import *


def ligand_center(residue):
    return np.mean(np.array([atom.coord for atom in residue.get_atoms()]), axis=0)

def is_valid_ligand(ligand_residue, struct, cutoff=10, min_pocket_size=4):
    #no ions
    if ligand_residue.resname in ["HOH", "NCO", "EPE"] or len(ligand_residue.resname) != 3:
        return False

    #get all residues within cutoff
    kd = NeighborSearch(list(struct.get_atoms()))
    center = ligand_center(ligand_residue)
    pocket = kd.search(ligand_center(ligand_residue), cutoff, level='R')

    #if not enough residues near ligand
    if len(pocket) < min_pocket_size:
        return False
    #if there is protein pocket is no bueno
    for res in pocket:
        if res.resname.strip() not in ["A", "U", "C", "G"] and res.resname != ligand_residue.resname:
            return False
    return True

def get_binding(strucpath):
    """
    Extracts binding pocket for a given PDB.

    TODO: add option to write PDB or return list of binding residues.
    """
    #load mmCIF structure
    struc_dict = MMCIF2Dict.MMCIF2Dict(strucpath)
    #load PDB
    parser = MMCIFParser(QUIET=True)
    pdbstruc = parser.get_structure("", strucpath)

    ligand_dict = {}
    try:
        ligand_dict['position'] = struc_dict['_pdbx_nonpoly_scheme.pdb_seq_num']
        ligand_dict['res_name'] = struc_dict['_pdbx_nonpoly_scheme.mon_id']
        ligand_dict['chain'] = struc_dict['_pdbx_nonpoly_scheme.pdb_strand_id']
        ligand_dict['unique_id'] = struc_dict['_pdbx_nonpoly_scheme.asym_id']

    except:
        print("Ligand not detected.")

    model = pdbstruc[0]
    try:
        ligand_df = pd.DataFrame.from_dict(ligand_dict)
    #pandas complains when dictionary values are not lists
    #this happens when there is only one ligand in PDB
    except ValueError:
        ligand_df = pd.DataFrame(ligand_dict, index=[0])

    ligand_df['position'] = pd.to_numeric(ligand_df['position'])
    pdbid = os.path.basename(strucpath).split(".")[0]
    ligand_df['pdbid'] = pdbid

    #check ligands
    invalid_ligands = 0
    valid_ligands = []
    for ligand in ligand_df.itertuples():
        ligand_res = None
        #find the residue corresponding to ligand
        for res in model[ligand.chain].get_residues():
            if res.id[1] == ligand.position:
                ligand_res = res
                if is_valid_ligand(ligand_res, model):
                    valid_ligands.append(ligand_res)
                else:
                    invalid_ligands += 1
    return valid_ligands

if __name__ == "__main__":
    PDB_PATH = os.path.join("..", "data", "sample_complexes")
    pdbs = [os.path.join(PDB_PATH, p) for p in os.listdir(PDB_PATH)]
    lig_list = []
    for i, p in enumerate(pdbs):
        print(p)
        ligs = list(get_binding(p))
        print(ligs)
    # all_ligands = pd.concat(lig_list)
    # all_ligands.to_csv("binding_sites_3A_interchain.csv")
    pass
