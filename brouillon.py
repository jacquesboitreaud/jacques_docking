# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:28:18 2019

@author: jacqu
"""

import os
import sys
import subprocess
import pybel, openbabel
import chimera

# Make mol2 ligands input file 

smi = 'COc1ccccc1OC(=O)Oc1ccccc1OC'

with open('../data/ligands/mymols.mol2', 'w') as f:
    mol = pybel.readstring("smi", smi)
    mol.addh()
    mol.make3D()
    txt = mol.write('mol2')
    f.write(txt)
f.close()


# Do docking : no target preparation to do. Generates dock input file.

docking(pdb_path, write_dir, ligands_path, dock_path)

# Most parameters (ligand file) are in rigid_train.in. Change before launch.

# Reading scores : 

