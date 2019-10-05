# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 12:46:22 2019

@author: jacqu

Reading top targets' data in binding db database.
Compare the binding scores computed to these assayed values 
 
"""
from main_np import main
import pandas as pd 
import argparse
import uuid
import numpy as np



# Most frequent targets 

top = pd.read_csv('/home/mcb/jboitr/data/top100.csv')
targets = np.unique(list(top['target']))

# Find all drugs which have esr1 aff data in BDB

esr1=top[top['target']=='Estrogen receptor']

esr_kis = esr1.loc[:,['SMILES','Ki']]

# Drop all which don't have a KI and sort from bigger to smaller 
esr_kis=esr_kis.dropna()
esr_kis = esr_kis.sort_values(by='Ki', axis=0, ascending=False)

# Launch docking for these molecules 

smiles = list(esr_kis['SMILES'])

parser=argparse.ArgumentParser()
parser.add_argument("-n", "--name", default=str(uuid.uuid4())[:8], help="Run ID. (default random ID)")
parser.add_argument("-i", "--pdb", default='esr1', help="DUD identifier of target to dock")
parser.add_argument("-d", "--dock-path", default='/home/mcb/jboitr/dock/dock6/bin', help="Path to dock install.")
parser.add_argument("-m", "--molecule-type", default='protein', help="Type of receptor (rna, or protein).")
parser.add_argument("-a", "--amber-scoring", default=False, help="Use slower but more accurate AMBER scoring.")
parser.add_argument("-p", "--params-path", default='/home/mcb/jboitr/dock/dock6/parameters', help="Path to param files.")
parser.add_argument("-s", "--smiles", default='c1ccccc1', help="SMILES string of ligand to dock")
args = parser.parse_args()

args.smiles=smiles

main(args)







