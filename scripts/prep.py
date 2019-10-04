"""
    Prepare receptor and ligand for docking, using Chimera 
"""
import sys
import os
import chimera
from chimera import runCommand

from utils import add_suffix_new_path 

def receptor(pdb_path, write_path):
    """
        Prepare receptor.
    """
    runCommand("open %s" % pdb_path)
    runCommand("delete ligand")
    runCommand("delete ions")
    runCommand("addh")
    runCommand("addcharge all method gas")
    runCommand("write format mol2 #0 %s" % add_suffix_new_path(pdb_path, write_path, "_rec_withH.mol2"))
    runCommand("write format pdb #0 %s" % add_suffix_new_path(pdb_path, write_path, "_rec_withH.pdb"))
    pass

def ligand(pdb_path, write_path):
    """
        Prepare biological ligand (if contained in the PBD file)
    """
    runCommand("open %s" % pdb_path)
    runCommand("delete ~ligand")
    runCommand("delete ions")
    runCommand("addh")
    runCommand("addcharge all method gas")
    runCommand("write format mol2 #1 %s" % add_suffix_new_path(pdb_path,write_path, "_lig_withH.mol2"))
    pass

def run(pdb_path):
    receptor(pdb_path)

pdb_path = sys.argv[1]
write_dir = sys.argv[2]
print (pdb_path)
print (write_dir)
receptor(pdb_path, write_dir)
# Uncomment ligand line to do the ligand part
#ligand(pdb_path, write_dir)
pass
