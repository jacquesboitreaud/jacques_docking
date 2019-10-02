# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 19:42:53 2019

@author: jacqu

Master docking script
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
    parser.add_argument("-i", "--pdb", default='data/pockets', help="Folder containing PDBs to dock")
    parser.add_argument("-l", "--lib", default='data/library.mol2', help="mol2 file containing ligands")
    parser.add_argument("-d", "--dock-path", default='/home/mcb/jboitr/dock/dock6', help="Path to dock install.")
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


    for pdbid in os.listdir(args.pdb):

        print(">>> PREPARING RECEPTOR")
        subprocess.call(['chimera', '--nogui', '--script',
            f'scripts/prep.py {os.path.join(args.pdb, pdbid)} {dock_files}'])
    
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

