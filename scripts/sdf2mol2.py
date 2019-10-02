import os
import shutil
from chimera import runCommand

def to_mol2(sdf_dir):
    """
        Use chimera to convert all sdf files in `sdf_dir` to mol2. 
    """
    for sdf in os.listdir(sdf_dir):
        try:
            runCommand("open %s" % os.path.join(sdf_dir, sdf))
            # runCommand("minimize")
            runCommand("write format mol2 0 " + os.path.join(sdf_dir, sdf[:-4]) + ".mol2")
            runCommand("close all")
        except:
            print "skipping %s" % sdf

    #place in single file
def cat(dest, file_dir, extension='.mol2'):
    with open(dest , 'w') as big_file:
        for f in os.listdir(file_dir):
            _, ext = os.path.splitext(f)
            if ext == extension:
                with open(os.path.join(file_dir, f)) as ff:
                    shutil.copyfileobj(ff, big_file)
if __name__ == "__main__":
    to_mol2('all_rna_prot_lig_sdfs_2019')
    cat('all.mol2', 'all_rna_prot_lig_sdfs_2019')
    pass
