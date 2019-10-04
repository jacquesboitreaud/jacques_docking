import os
import os.path as osp
import subprocess

from scripts.utils import *

"""
Update : 
Modified the input file to compute both energy and contact grids 
"""

def box(pdb_path, write_dir):
    params = f"""Y
8.0
{osp.join(write_dir, 'selected_spheres.sph')}
1
{add_suffix_new_path(pdb_path, write_dir, '.box.pdb')}"""

    with open(f"{osp.join(write_dir, 'showbox.in')}", "w") as box:
        print(params)
        box.write(params)
    print(">>> SHOWBOX")
    cmd = f"showbox < {osp.join(write_dir, 'showbox.in')}"
    print(cmd)
    os.system(cmd)

def grid(pdb_path, write_dir, dock_path, params_path):
    params = f"""compute_grids        yes
grid_spacing                              0.4
output_molecule                           no
contact_score                             yes
energy_score                              yes
energy_cutoff_distance                    9999
atom_model                                a
attractive_exponent                       6
repulsive_exponent                        12
distance_dielectric                       yes
dielectric_factor                         4
bump_filter                               yes
bump_overlap                              0.75
receptor_file                             {add_suffix_new_path(pdb_path, write_dir, '_rec_withH.mol2')}
box_file                                  {add_suffix_new_path(pdb_path, write_dir, '.box.pdb')}
vdw_definition_file                       {params_path}/parameters/vdw_AMBER_parm99.defn
score_grid_prefix                         grid
"""
    
    with open(osp.join(write_dir, "grid.in"), "w") as box:
        box.write(params)
    subprocess.call(["grid", "-i", f"{osp.join(write_dir, 'grid.in')}", "-o", f"{osp.join(write_dir, 'gridinfo.out')}"])
    pass

