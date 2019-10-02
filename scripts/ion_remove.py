import os
import sys

"""
Kill SDF files with ions PDBID_MOLNAME_...sdf
"""

folder = sys.argv[1]

for f in os.listdir(folder):
    if len(f.split("_")[1]) < 3:
        os.remove(os.path.join(folder, f))
