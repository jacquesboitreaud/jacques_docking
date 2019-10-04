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
import pandas as pd

from scripts.spheres import spheres
from scripts.boxgrid import box, grid
from scripts.dock import minimize, contact_docking
from scripts.get_ligands import from_smiles, from_smiles_list
from scripts.score import parse_scores


def cline():

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name", default=str(uuid.uuid4())[:8], help="Run ID. (default random ID)")
    parser.add_argument("-i", "--pdb", default='esr1', help="DUD identifier of target to dock")
    parser.add_argument("-d", "--dock-path", default='/home/mcb/jboitr/dock/dock6/bin', help="Path to dock install.")
    parser.add_argument("-m", "--molecule-type", default='protein', help="Type of receptor (rna, or protein).")
    parser.add_argument("-a", "--amber-scoring", default=False, help="Use slower but more accurate AMBER scoring.")
    parser.add_argument("-p", "--params-path", default='/home/mcb/jboitr/dock/dock6/parameters', help="Path to param files.")
    parser.add_argument("-s", "--smiles", default='c1ccccc1', help="SMILES string of ligand to dock")

    args = parser.parse_args()

    df=main(args)
    
    return df


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
    if(type(args.smiles)==str):
        from_smiles(args.smiles)
    elif(type(args.smiles)==list):
        from_smiles_list(args.smiles)
    else:
        print('Unsupported smiles input')
        return

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
            
            print(">>> PARSING SCORES")
            sc = parse_scores(writedir)
            
            df = pd.DataFrame.from_dict({'can':args.smiles,
                                         str(pdbid): sc})
            df.to_csv(os.path.join('/home/mcb/jboitr/data/scores',pdbid,'.csv'))
            
            return df


if __name__ == "__main__":
    cline()

pass

