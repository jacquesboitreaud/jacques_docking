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
        Prepare receptor:
            Opens DUD/target/receptor.pdb
            Saves to dock_files/rec_with_H...
    """
    runCommand("open %s" % pdb_path)
    runCommand("delete ligand")
    runCommand("delete ions")
    runCommand("addh")
    runCommand("addcharge all method gas")
    runCommand("write format mol2 #0 %s" % os.path.join(write_path, "rec_withH.mol2"))
    runCommand("write format pdb #0 %s" % os.path.join(write_path,"rec_withH.pdb"))
    pass

def ligand(lig_path, write_path):
    """
        Prepare biological ligand
        Opens ligand pdb path (TO DEFINE)
        Saves in dock_files/lig_withH.mol2
    """
    runCommand("open %s" % pdb_path)
    runCommand("delete ~ligand")
    runCommand("delete ions")
    runCommand("addh")
    runCommand("addcharge all method gas")
    runCommand("write format mol2 #1 %s" % os.path.join(write_path, "lig_withH.mol2"))
    pass

def run(pdb_path):
    receptor(pdb_path)

pdb_path = sys.argv[1]
write_dir = sys.argv[2]
ligand_path = sys.argv[3]
print (pdb_path)
print (write_dir)
receptor(pdb_path, write_dir)
ligand(ligand_path, write_dir)
pass
