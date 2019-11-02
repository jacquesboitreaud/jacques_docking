# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 12:45:16 2019

@author: jacqu

Script to extract ligands and decoys for a certain DUDE target (esr1 by default)
and saves to CSV
"""


import pandas as pd 
import os 
import numpy as np


TARGET = 'esr1'
dud_repo = 'C:/Users/jacqu/Documents/mol2_resource/dud/all'
os.chdir(dud_repo)

dict_a, dict_d= {}, {}

for target_folder in os.listdir(dud_repo):
    if(target_folder==TARGET):
        a_smiles, d_smiles = [], []
        
        with open(f'{target_folder}/actives_final.ism', 'r') as f : 
            actives = f.readlines()
            for l in actives :
                s=l.split(' ')[0]
                if('9' in s or 'p' in s or ' ' in s or '.' in s or len(s)>150):
                    next
                else:
                    a_smiles.append(s)
            
    
        with open(f'{target_folder}/decoys_final.ism', 'r') as f : 
            dec = f.readlines()
            for l in dec :
                s=l.split(' ')[0]
                if('9' in s or 'p' in s or ' ' in s or '.' in s or len(s)>150):
                    next
                else:
                    d_smiles.append(s)
   
         
DUD_test={'a':a_smiles,'d':d_smiles}
        
# Save dicts to data
np.save('C:/Users/jacqu/Documents/GitHub/jacques_docking/DUD_test.npy', DUDE_test)