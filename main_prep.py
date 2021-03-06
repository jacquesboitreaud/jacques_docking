# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 19:42:53 2019

@author: jacqu

Master script for only processing targets. No docking.  
    
"""


import os
import sys
import subprocess
import argparse
import uuid


from scripts.spheres import spheres
from scripts.boxgrid import box, grid
from scripts.dock import minimize, contact_docking
from scripts.get_ligands import from_smiles


def cline():

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name", default=str(uuid.uuid4())[:8], help="Run ID. (default random ID)")
    parser.add_argument("-i", "--pdb", default='/home/mcb/jboitr/jacques_docking/targets', help="Folder containing PDBs to dock")
    parser.add_argument("-l", "--lib", default='/home/mcb/jboitr/data/ligands/library.mol2', help="mol2 file containing ligands")
    parser.add_argument("-d", "--dock-path", default='/home/mcb/jboitr/dock/dock6/bin', help="Path to dock install.")
    parser.add_argument("-m", "--molecule-type", default='protein', help="Type of receptor (rna, or protein).")
    parser.add_argument("-a", "--amber-scoring", default=False, help="Use slower but more accurate AMBER scoring.")
    parser.add_argument("-s", "--smiles", default='c1ccccc1', help="SMILES string of ligand to dock")
    parser.add_argument("-p", "--params-path", default='/home/mcb/jboitr/dock/dock6/parameters', help="Path to param files.")

    args = parser.parse_args()

    main(args)


def main(args):


    dock_path = args.dock_path
    params_path = args.params_path
    DUD_path = '/home/mcb/jboitr/data/all'


    for pdbid in os.listdir(DUD_path):
        
        if(pdbid!='esr1'):
            # ONLY ONE FOR TESTING !
            next
        else:
        
            # Get receptor name : 
            target_dir=os.path.join(DUD_path,pdbid)
            try:
                os.mkdir(f'{target_dir}/dock_files')
            except:
                pass
            
            # 1/ Prepare receptor and ligand
            dock_files = f'{target_dir}/dock_files'
            pdb_path = f'{target_dir}/receptor.pdb'
            ligand_path = f'{target_dir}/crystal_ligand.mol2'
            
            
            print(">>> PREPARING RECEPTOR")
            subprocess.call(['chimera', '--nogui', '--script',
                f'scripts/prep.py {pdb_path} {dock_files} {ligand_path}'])
            
            """
            # 2/ Create spheres in binding site 
            dms_in = f'{dock_files}/rec_withH.pdb'
            print(">>> CREATING SPHERES")
            spheres(dms_in, dock_files)
            """
            
            # 3 / Creating box around binding site
            print(">>> CREATING BOX")
            box(pdb_path, dock_files)
            
            
            # 4 / Creating grids for scoring
            print(">>> CREATING GRID")
            grid(pdb_path, dock_files, dock_path, params_path)
            

if __name__ == "__main__":
    cline()

pass

