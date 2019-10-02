import subprocess
import os
import os.path as osp

from utils import *

""" Generates spheres with DMS """

def spheres(pdb_path, write_dir):
    dms_path = add_suffix_kill_prefix(pdb_path, ".dms")
    sphere_path = add_suffix_kill_prefix(pdb_path, '_rec.sph')
    dms_in = add_suffix_kill_prefix(pdb_path, "_rec_withH.pdb")

    root = os.getcwd()
    os.chdir(write_dir)
    print(">>> Calling DMS")
    #generate surface
    subprocess.call(["dms",  dms_in  , "-a", "-n", "-o", 
        dms_path])

    params = f"""{dms_path}
R
X
0.0
4.0
1.4
{sphere_path}"""

    with open("INSPH", "w") as sph:
        sph.write(params)
    #generate spheres
    print(">>> Calling sphgen")
    subprocess.call(["sphgen", "-i", "INSPH", "-o", f"OUTSPH"])

    print(">>> Calling sphere_selector")
    #select on binding site
    subprocess.call(["sphere_selector", sphere_path,\
        f"{add_suffix_kill_prefix(pdb_path, '_lig_withH.mol2')}",  "10.0"])
    os.chdir(root)
    pass
