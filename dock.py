# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 18:20:49 2019

@author: jacqu
"""
from main_np import main
import pandas as pd 
import argparse 


df = pd.read_csv('/home/mcb/jboitr/data/moses_test.csv', nrows = 100)

smiles = df['can']

parser=argparse.ArgumentParser()
parser.add_argument("-s", "--smiles", default='c1ccccc1', help="SMILES string of ligand to dock")
args = parser.parse_args()

main(args)

