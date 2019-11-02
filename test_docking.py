# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 18:20:49 2019

@author: jacqu
"""
from main_np import main
import numpy as np
import argparse
import uuid


test_mols = np.load('DUDE_test.npy', allow_pickle=True).item()

actives = list(test_mols['a'])
decoys = list(test_mols['d'])

# Start with docking actives
smiles = actives

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

