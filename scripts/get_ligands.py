"""
    Extract ligands from full PDB.
    Produces folder with:
        - cleaned receptor PDB (with just RNA)
        - mol2 for each ligand
"""
import os
import sys
import pybel

if __name__ == "__main__":
    sys.path.append('..')


#from chimera import runCommand as rc

def complex_process(pdb_path, dump_path, distance=5):
    """
        Prepare one complex for re-docking and get ligand.
        If protein, gets ligands further than `distance` from protein.
    """

    prefix, suffix = os.path.basename(pdb_path).split(".")

    rc("open %s" % pdb_path)

    print (">>> Opened model")

    #select ligands within cutoff and far from protein
    rc("select ligand & nucleic acid z<%d"% distance)
    rc("~select protein z<%d"% distance)
    rc("~select ions")

    print (">>> Made selection")

    #get selected ligands
    rc("writesel %s" % os.path.join(dump_path, 'sel.txt'))

    print (">>> Wrote selection")
    #no valid ligands found (empty selection)
    if os.stat(os.path.join(dump_path, 'sel.txt')).st_size == 0:
        return 1
    #prep
    #rc("delete ions")
    rc("addh")
    rc("addcharge all method gas")

    main_model = "#0"
    with open(os.path.join(dump_path, "sel.txt"), "r") as sel:
        unique_residues = set()
        for res in sel:
            print (">>> writing ligand %s" % res)
            s = res.strip()
            model, res = s.split(":")
            main_model = model
            #make sure we don't add multiple copies of the same ligand
            if res not in unique_residues:
                rc("select %s" % s)
                s = "".join(s.split())
                rc("write format mol2 selected %s %s" % (model, os.path.join(dump_path, 'ligands', prefix + "_" + s + ".mol2")))
                unique_residues.add(res)

    #save receptor pdb, mol2
    rc("delete ligand")
    rc("write format mol2 %s %s" % (main_model, os.path.join(dump_path, 'receptors', prefix + "_rec_withH.mol2")))
    rc("write format pdb %s %s" % (main_model, os.path.join(dump_path, 'receptors',  prefix + "_rec_withH.pdb")))

    return 0

def create_library(complexes, dump_path):
    """
        Takes complexes, prepares each one and creates library of all ligands.
    """

    try:
        os.mkdir(os.path.join(dump_path, 'receptors'))
        os.mkdir(os.path.join(dump_path, 'ligands'))
    except:
        pass

    failures = 0
    for complex in os.listdir(complexes):
        pdb_path = os.path.join(complexes, complex)
        result = complex_process(pdb_path, dump_path)
        failures += result
        print (">>> Failed on %d" % failures)
    pass

if __name__ == "__main__":
    create_library("../data/sample_complexes", "../data/test/")
    pass

def from_smiles(smi):
    """
    Takes SMILES string, generate m3D rpz in mol2 format, adds Hs and saves
    """
    with open('../data/ligands/library.mol2', 'w') as f:
        mol = pybel.readstring("smi", smi)
        mol.addh()
        mol.make3D()
        txt = mol.write('mol2')
        f.write(txt)
         
        f.close()
