# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 18:20:49 2019

@author: jacqu
"""
from main_np import cline
import pandas as pd 

df = pd.read_csv('/home/mcb/jboitr/data/moses_test.csv', nrows = 1000)

smiles = df['can']

cline(smiles = smiles)

