# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:28:18 2019

@author: jacqu

Main script to perform DOCK contact scoring given an input SMILES of a ligand

"""

import os
import sys
sys.path.append('../')
sys.path.append('../scripts')

import subprocess
import pybel
import argparse
import uuid

from scripts.dock import minimize_contact, contact_docking
from scripts.get_ligands import from_smiles

def cline():

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name", default=str(uuid.uuid4())[:8], help="Run ID. (default random ID)")
    parser.add_argument("-i", "--pdb", default='/home/mcb/jboitr/data/pockets', help="Folder containing PDBs to dock")
    parser.add_argument("-s", "--smiles", default='c1ccccc1', help="SMILES string of ligand to dock")
    parser.add_argument("-l", "--lib", default='/home/mcb/jboitr/data/ligands/mymols.mol2', help="mol2 file containing ligands")
    parser.add_argument("-d", "--dock-path", default='/home/mcb/jboitr/dock/dock6/bin', help="Path to dock install.")
    parser.add_argument("-p", "--parameters-path", default='/home/mcb/jboitr/dock/dock6/parameters', help="Path to dock params.")
    parser.add_argument("-m", "--molecule-type", default='protein', help="Type of receptor (rna, or protein).")
    parser.add_argument("-a", "--amber-scoring", default=False, help="Use slower but more accurate AMBER scoring.")
    args = parser.parse_args()

    main(args)
    
def main(args):
    # Create repository for the run and the generated files 
    try:
        os.mkdir(f'runs/{args.name}')
        os.mkdir(f'runs/{args.name}/dock_files')
    except:

        pass


    dock_files = f'runs/{args.name}/dock_files'
    dock_path = args.dock_path
    params_path=args.parameters_path
    pdb_path = args.pdb
    
    print(">>> GENERATING LIGAND MOL2")
    from_smiles(args.smiles)

    for pdbid in os.listdir(pdb_path):
        

        print(">>> MINIMIZING")
        minimize_contact(pdb_path, pdbid, dock_files, args.lib, dock_path, params_path)

        print(">>> DOCKING")
        contact_docking(pdb_path, pdbid, dock_files, args.lib, dock_path, params_path)


if __name__ == "__main__":
    sys.path.append("..")
    cline()

pass

"""
smi = 'COc1ccccc1OC(=O)Oc1ccccc1OC'

# Reading scores : 
"""
