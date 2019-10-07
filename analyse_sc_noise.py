# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 14:30:39 2019

@author: jacqu

Analyse noise due to the conformation sampling of the molecule
"""

# Take top 100 molecules of one target, dock them 10 times 

import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

from main_np import main
import pandas as pd 
import argparse
import uuid
import numpy as np

# Load csv 
df = pd.read_csv('/home/mcb/jboitr//data/moses_train.csv', nrows=400000)

# Get top scoring smiles
by_esr1 = df.sort_values(by = 'esr1')
top_esr1 = by_esr1[:100]
smi = list(top_esr1['can'])

# DOCK the smiles 

parser=argparse.ArgumentParser()
parser.add_argument("-n", "--name", default=str(uuid.uuid4())[:8], help="Run ID. (default random ID)")
parser.add_argument("-i", "--pdb", default='esr1', help="DUD identifier of target to dock")
parser.add_argument("-d", "--dock-path", default='/home/mcb/jboitr/dock/dock6/bin', help="Path to dock install.")
parser.add_argument("-m", "--molecule-type", default='protein', help="Type of receptor (rna, or protein).")
parser.add_argument("-a", "--amber-scoring", default=False, help="Use slower but more accurate AMBER scoring.")
parser.add_argument("-p", "--params-path", default='/home/mcb/jboitr/dock/dock6/parameters', help="Path to param files.")
parser.add_argument("-s", "--smiles", default='c1ccccc1', help="SMILES string of ligand to dock")
args = parser.parse_args()

args.smiles=smi

main(args)