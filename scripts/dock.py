import subprocess

from .utils import *

def minimize(pdb_path, write_dir, dock_path): 
    params = f"""conformer_search_type       rigid
use_internal_energy                                          yes
internal_energy_rep_exp                                      12
internal_energy_cutoff                                       100.0
ligand_atom_file                                             {add_suffix_new_path(pdb_path, write_dir, '_lig_withH.mol2')}
limit_max_ligands                                            no
skip_molecule                                                no
read_mol_solvation                                           no
calculate_rmsd                                               yes
use_rmsd_reference_mol                                       {add_suffix_new_path(pdb_path, write_dir, '_lig_withH.mol2')}
use_database_filter                                          no
orient_ligand                                                no
bump_filter                                                  no
score_molecules                                              yes
contact_score_primary                                        no
contact_score_secondary                                      no
grid_score_primary                                           yes
grid_score_secondary                                         no
grid_score_rep_rad_scale                                     1
grid_score_vdw_scale                                         1
grid_score_es_scale                                          1
grid_score_grid_prefix                                       grid
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
vdw_defn_file                                                {osp.join(dock_path, 'parameters/vdw_AMBER_parm99.defn')}
flex_defn_file                                               {osp.join(dock_path, 'parameters/flex.defn')}
flex_drive_file                                              {osp.join(dock_path, 'parameters/flex_drive.tbl')}
ligand_outfile_prefix                                        {add_suffix_new_path(pdb_path, write_dir, '.lig.min')}
write_orientations                                           no
num_scored_conformers                                        1
rank_ligands                                                 no
"""

    with open(osp.join(write_dir, "min.in"), "w") as m:
        m.write(params)

    subprocess.call(["dock6", "-i", osp.join(write_dir, "min.in")])


def docking(pdb_path, write_dir, ligands_path, dock_path):

    params = f"""conformer_search_type              rigid
use_internal_energy                                          yes
internal_energy_rep_exp                                      12
internal_energy_cutoff                                       100.0
ligand_atom_file                                             {ligands_path} 
limit_max_ligands                                            no
skip_molecule                                                no
read_mol_solvation                                           no
calculate_rmsd                                               yes
use_rmsd_reference_mol                                       {add_suffix_new_path(pdb_path, write_dir, '.lig.min_scored.mol2')}
use_database_filter                                          no
orient_ligand                                                yes
automated_matching                                           yes
receptor_site_file                                           {osp.join(write_dir, 'selected_spheres.sph')}
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
grid_score_grid_prefix                                       grid
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
vdw_defn_file                                                {osp.join(dock_path, 'parameters/vdw_AMBER_parm99.defn')}
flex_defn_file                                               {osp.join(dock_path, 'parameters/flex.defn')}
flex_drive_file                                              {osp.join(dock_path, 'parameters/flex_drive.tbl')}
ligand_outfile_prefix                                        {osp.join(write_dir, 'rigid.out')}
write_orientations                                           no
num_scored_conformers                                        1
rank_ligands                                                 no
"""

    with open(osp.join(write_dir, "rigid.in"), "w") as r:
        r.write(params)
    subprocess.call(["dock6", "-i", osp.join(write_dir, "rigid.in")])

def amber_dock(receptor_prefix, ligand_path, work_dir):
    root = os.getcwd()
    os.chdir(work_dir)

    params = f"""conformer_search_type                                        rigid
use_internal_energy                                          no
ligand_atom_file                                             {add_suffix(ligand_path, '.amber_score.mol2')}
limit_max_ligands                                            no
skip_molecule                                                no
read_mol_solvation                                           no
calculate_rmsd                                               no
use_database_filter                                          no
orient_ligand                                                no
bump_filter                                                  no
score_molecules                                              yes
contact_score_primary                                        no
contact_score_secondary                                      no
grid_score_primary                                           no
grid_score_secondary                                         no
multigrid_score_primary                                      no
multigrid_score_secondary                                    no
dock3.5_score_primary                                        no
dock3.5_score_secondary                                      no
continuous_score_primary                                     no
continuous_score_secondary                                   no
footprint_similarity_score_primary                           no
footprint_similarity_score_secondary                         no
pharmacophore_score_primary                                  no
pharmacophore_score_secondary                                no
descriptor_score_primary                                     no
descriptor_score_secondary                                   no
gbsa_zou_score_primary                                       no
gbsa_zou_score_secondary                                     no
gbsa_hawkins_score_primary                                   no
gbsa_hawkins_score_secondary                                 no
SASA_score_primary                                           no
SASA_score_secondary                                         no
amber_score_primary                                          yes
amber_score_secondary                                        no
amber_score_receptor_file_prefix                             {receptor_prefix}
amber_score_movable_region                                   ligand
amber_score_minimization_rmsgrad                             0.01
amber_score_before_md_minimization_cycles                    100
amber_score_md_steps                                         3000
amber_score_after_md_minimization_cycles                     100
amber_score_gb_model                                         5
amber_score_nonbonded_cutoff                                 18.0
amber_score_temperature                                      300.0
amber_score_abort_on_unprepped_ligand                        yes
ligand_outfile_prefix                                        output
write_orientations                                           no
num_scored_conformers                                        1
rank_ligands                                                 no
"""

    subprocess.call(['dock6', 'dock.in'])

    os.chidr(root)
    pass
