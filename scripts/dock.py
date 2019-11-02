import subprocess

from .utils import *

##### TODO  : change parameters to add bump filter. 
# The following parameters should be added 
"""
bump_grid_prefix                                             {osp.join(dock_files_path,"grid")}
max_bumps_anchor                                             2
max_bumps_growth                                             2
"""

# Functions 

def minimize(dock_files_path, write_dir, dock_path, params_path): 
    params = f"""conformer_search_type       flex
user_specified_anchor                                        no
limit_max_anchors                                            yes
max_anchor_num                                               1
min_anchor_size                                              5
pruning_use_clustering                                       yes
pruning_max_orients                                          100
pruning_clustering_cutoff                                    100
use_clash_overlap                                            yes
clash_overlap                                                1
use_internal_energy                                          yes
internal_energy_rep_exp                                      12
internal_energy_cutoff                                       100.0
ligand_atom_file                                             /home/mcb/jboitr/data/ligands/library.mol2
limit_max_ligands                                            no
skip_molecule                                                no
read_mol_solvation                                           no
calculate_rmsd                                               yes
use_rmsd_reference_mol                                       no
use_database_filter                                          no
orient_ligand                                                yes
automated_matching                                           yes
receptor_site_file                                           {osp.join(dock_files_path, 'selected_spheres.sph')}
receptor_site_file                                           {osp.join(dock_files_path, 'selected_spheres.sph')}
max_orientations                                             1000
critical_points                                              no
chemical_matching                                            no
use_ligand_spheres                                           no
bump_filter                                                  no
score_molecules                                              yes
contact_score_primary                                        no
contact_score_secondary                                      no
grid_score_primary                                           yes
grid_score_secondary                                         no
grid_score_rep_rad_scale                                     1
grid_score_vdw_scale                                         1
grid_score_es_scale                                          1
grid_score_grid_prefix                                       {osp.join(dock_files_path,"grid")}
multigrid_score_secondary                                    no
dock3.5_score_secondary                                      no
continuous_score_secondary                                   no
footprint_similarity_score_secondary                         no
pharmacophore_score_secondary                                no
descriptor_score_secondary                                   no
gbsa_zou_score_secondary                                     no
gbsa_hawkins_score_secondary                                 no
SASA_score_secondary                                         no
amber_score_secondary                                        no
minimize_ligand                                              yes
simplex_max_iterations                                       1000
simplex_tors_premin_iterations                               0
simplex_max_cycles                                           1
simplex_score_converge                                       0.1
simplex_cycle_converge                                       1.0
simplex_trans_step                                           1.0
simplex_rot_step                                             0.1
simplex_tors_step                                            10.0
simplex_random_seed                                          0
simplex_restraint_min                                        yes
simplex_coefficient_restraint                                10.0
atom_model                                                   all
vdw_defn_file                                                {osp.join(params_path, 'vdw_AMBER_parm99.defn')}
flex_defn_file                                               {osp.join(params_path, 'flex.defn')}
flex_drive_file                                              {osp.join(params_path, 'flex_drive.tbl')}
ligand_outfile_prefix                                        {osp.join(write_dir, 'lig.min')}
write_orientations                                           no
num_scored_conformers                                        1
rank_ligands                                                 no
"""

    with open(osp.join(write_dir, "min.in"), "w") as m:
        m.write(params)

    subprocess.call(["dock6.mpi", "-i", osp.join(write_dir, "min.in")])


def contact_docking(dock_files_path, write_dir, dock_path, params_path):
    # Contact scoring only
    # Uses the minimized ligand mol2, computed previously and stored in the run's directory (write_dir).

    params = f"""conformer_search_type              flex
user_specified_anchor                                        no
limit_max_anchors                                            yes
max_anchor_num                                               1
min_anchor_size                                              5
pruning_use_clustering                                       yes
pruning_max_orients                                          100
pruning_clustering_cutoff                                    100
use_clash_overlap                                            yes
clash_overlap                                                1
use_internal_energy                                          yes
internal_energy_rep_exp                                      12
internal_energy_cutoff                                       100.0
ligand_atom_file                                             {osp.join(write_dir, 'lig.min_scored.mol2')}
limit_max_ligands                                            no
skip_molecule                                                no
read_mol_solvation                                           no
calculate_rmsd                                               yes
use_rmsd_reference_mol                                       no
use_database_filter                                          no
orient_ligand                                                yes
automated_matching                                           yes
receptor_site_file                                           {osp.join(dock_files_path, 'selected_spheres.sph')}
max_orientations                                             1000
critical_points                                              no
chemical_matching                                            no
use_ligand_spheres                                           no
bump_filter                                                  no
score_molecules                                              yes
contact_score_primary                                        yes
contact_score_secondary                                      no
contact_score_cutoff_distance 	                             4.5
contact_score_clash_overlap 	                             0.75
contact_score_clash_penalty 	                             50
contact_score_grid_prefix 	 	                             {osp.join(dock_files_path,"grid")}
grid_score_primary                                           no
grid_score_secondary                                         no
multigrid_score_secondary                                    no
dock3.5_score_secondary                                      no
continuous_score_secondary                                   no
footprint_similarity_score_secondary                         no
pharmacophore_score_secondary                                no
descriptor_score_secondary                                   no
gbsa_zou_score_secondary                                     no
gbsa_hawkins_score_secondary                                 no
SASA_score_secondary                                         no
amber_score_secondary                                        no
minimize_ligand                                              yes
simplex_max_iterations                                       1000
simplex_tors_premin_iterations                               0
simplex_max_cycles                                           1
simplex_score_converge                                       0.1
simplex_cycle_converge                                       1.0
simplex_trans_step                                           1.0
simplex_rot_step                                             0.1
simplex_tors_step                                            10.0
simplex_random_seed                                          0
simplex_restraint_min                                        no
atom_model                                                   all
vdw_defn_file                                                {osp.join(params_path, 'vdw_AMBER_parm99.defn')}
flex_defn_file                                               {osp.join(params_path, 'flex.defn')}
flex_drive_file                                              {osp.join(params_path, 'flex_drive.tbl')}
ligand_outfile_prefix                                        {osp.join(write_dir, 'flexible.out')}
write_orientations                                           no
num_scored_conformers                                        1
rank_ligands                                                 no
"""

    with open(osp.join(write_dir, "flexible.in"), "w") as r:
        r.write(params)
    subprocess.call(["dock6.mpi", "-i", osp.join(write_dir, "flexible.in"), "-o", osp.join(write_dir, "flexible.out")])
