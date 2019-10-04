# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 19:42:53 2019

@author: jacqu

Master docking script when target preprocessing is already done. 

STRUCTURE OF THE DUD DATABASE :
    /all : directory of all DUD targets 
    /all/target_ids : targets 
    /all/target_ids/dock_files : contains all dock preprocessing files
    
data/ligands/library.mol2 : all the ligands to dock
    
"""


import os
import sys
import subprocess
import argparse
import uuid


from scripts.spheres import spheres
from scripts.boxgrid import box, grid
from scripts.dock_np import minimize, docking, contact_docking
from scripts.get_ligands import from_smiles


def cline():

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name", default=str(uuid.uuid4())[:8], help="Run ID. (default random ID)")
    parser.add_argument("-i", "--pdb", default='/home/mcb/jboitr/data/pockets', help="Folder containing PDBs to dock")
    parser.add_argument("-l", "--lib", default='/home/mcb/jboitr/data/ligands/library.mol2', help="mol2 file containing ligands")
    parser.add_argument("-d", "--dock-path", default='/home/mcb/jboitr/dock/dock6/bin', help="Path to dock install.")
    parser.add_argument("-m", "--molecule-type", default='protein', help="Type of receptor (rna, or protein).")
    parser.add_argument("-a", "--amber-scoring", default=False, help="Use slower but more accurate AMBER scoring.")
    parser.add_argument("-s", "--smiles", default='c1ccccc1', help="SMILES string of ligand to dock")
    parser.add_argument("-p", "--params-path", default='/home/mcb/jboitr/dock/dock6/parameters', help="Path to param files.")

    args = parser.parse_args()

    main(args)


def main(args):
    # Create repository for the run and the generated files 
    try:
        os.mkdir(f'runs/{args.name}')
    except:

        pass

    dock_path = args.dock_path
    params_path = args.params_path
    DUD_path = '/home/mcb/jboitr/data/all'
    writedir = f'runs/{args.name}'
    
    # Building ligands mol2 file 
    print(">>> BUILDING LIGAND MOL2")
    from_smiles(args.smiles)

    for pdbid in os.listdir(DUD_path):
        
        if(pdbid!='esr1'):
            # ONLY ONE FOR TESTING !
            next
        else:
            
            dock_files_path=os.path.join(DUD_path,pdbid,'dock_files')
            print(">>> MINIMIZING")
            minimize(dock_files_path, writedir, dock_path, params_path)
    
            print(">>> DOCKING")
            contact_docking(dock_files_path, writedir, dock_path, params_path)


if __name__ == "__main__":
    cline()

pass

