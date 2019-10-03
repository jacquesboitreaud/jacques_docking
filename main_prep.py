# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 19:42:53 2019

@author: jacqu

Master docking script

TODO : 
    add the input smiles parameter to arguments
    create a contact_docking function
    change the grid computation to compute two grids (cnt and energy)
    Be careful the docking is done with the minimized ligand conformation (ligand input file & rmsd)
    
    Check all the path parameters if problems
    Check paths relatives to DOCK setup (/bin, /params)
    
    Check we get the same contact score when docking several times the same ligand 
    
"""


import os
import sys
import subprocess
import argparse
import uuid


from scripts.spheres import spheres

from scripts.boxgrid import box, grid

from scripts.dock import minimize, docking


def cline():

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name", default=str(uuid.uuid4())[:8], help="Run ID. (default random ID)")
    parser.add_argument("-i", "--pdb", default='/home/mcb/jboitr/data/pockets', help="Folder containing PDBs to dock")
    parser.add_argument("-l", "--lib", default='/home/mcb/jboitr/data/library.mol2', help="mol2 file containing ligands")
    parser.add_argument("-d", "--dock-path", default='/home/mcb/jboitr/dock/dock6/bin', help="Path to dock install.")
    parser.add_argument("-m", "--molecule-type", default='protein', help="Type of receptor (rna, or protein).")
    parser.add_argument("-a", "--amber-scoring", default=False, help="Use slower but more accurate AMBER scoring.")
    parser.add_argument("-s", "--smiles", default='c1ccccc1', help="SMILES string of ligand to dock")

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
    pdb_file='receptor.pdb'

    # gros problème, quand on met pdb_file ici ça l'ajoute en argument de la fonction  d'en dessous et ça change le nom du fichier écrit. 

    for pdbid in os.listdir(args.pdb):

        print(">>> PREPARING RECEPTOR")
        subprocess.call(['chimera', '--nogui', '--script',
            f'scripts/prep.py {os.path.join(args.pdb, pdbid, pdb_file)} {dock_files}'])
    
        print(">>> CREATING SPHERES")
        spheres(pdbid, dock_files)

        print(">>> CREATING BOX AND GRID")
        box(pdbid, dock_files)

        print(">>> CREATING GRID")
        grid(pdbid, dock_files, dock_path)

        print(">>> MINIMIZING")
        minimize(pdbid, dock_files, dock_path)

        print(">>> DOCKING")
        docking(pdbid, dock_files, args.lib, dock_path)


if __name__ == "__main__":
    cline()

pass

