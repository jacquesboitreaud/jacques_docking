# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 09:56:05 2019

@author: jacqu
"""

import pandas as pd
import seaborn as sns
import numpy as np

top = pd.read_csv('C:/Users/jacqu/Documents/data/bindingdb/top100.csv')
targets = np.unique(list(top['target']))

# Find all drugs which have esr1 aff data in BDB

esr1=top[top['target']=='Estrogen receptor']

esr_kis = esr1.loc[:,['SMILES','Ki']]

# Drop all which don't have a KI and sort from bigger to smaller 
esr_kis=esr_kis.dropna()
esr_kis = esr_kis.sort_values(by='Ki', axis=0, ascending=False)

# Read contact scores 
scores=[]
with open("C:/Users/jacqu/Documents/mol2_resource/rigid.out_scored.mol2", "r") as f:
      line = f.readline()
      while line:
          if('Contact_Score' in line):
              line = line.rstrip('\n')
              sc = float(line[-20:])
              if(sc>0):
                  sc=-sc
              scores.append(sc)
          line = f.readline()
   
esr_kis['scores']=pd.Series(scores, index = esr_kis.index)

# Plot contact score versus Ki (binding constant)
import matplotlib.pyplot as plt
sns.scatterplot(esr_kis['Ki'],esr_kis['scores'])
plt.xlabel('Ranked Ki for assayed ligands')
plt.ylabel('DOCK contact score')
plt.title('Contact score vs experimental Ki for 500 mols assayed vs ESR1')

