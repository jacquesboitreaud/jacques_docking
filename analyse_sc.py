# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 18:07:04 2019

@author: jacqu

Analyse scores to find top scoring compounds for each target and see if 
it is relevant 
"""

import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

# Load csv 
df = pd.read_csv('C:/Users/jacqu/Documents/GitHub/data/moses_train.csv', nrows=341000)

# Sort compounds by contact scores for each target 
by_ampc = df.sort_values(by = 'ampc')
by_cxcr4 = df.sort_values(by = 'cxcr4')
by_esr1 = df.sort_values(by = 'esr1')
by_gcr =df.sort_values(by= 'gcr')

# Select top scoring ampc compounds 
top_ampc = by_ampc[:1000]
sns.distplot(top_ampc['cxcr4'], label = 'cxcr4 score')
sns.distplot(top_ampc['ampc'], label = 'ampc score')
sns.distplot(top_ampc['esr1'], label = 'esr1 score')
sns.distplot(top_ampc['gcr'], label = 'gcr score')
plt.title('1k AMPC top-scored compounds')
plt.xlabel('contact scores')
plt.legend()

# Symetric operation for cxcr4 compounds : 
plt.figure()
top_cxcr4 = by_cxcr4[:1000]
sns.distplot(top_cxcr4['cxcr4'], label = 'cxcr4 score')
sns.distplot(top_cxcr4['ampc'], label = 'ampc score')
sns.distplot(top_cxcr4['esr1'], label = 'esr1 score')
sns.distplot(top_cxcr4['gcr'], label = 'gcr score')
plt.title('1k CXCR4 top-scored compounds')
plt.xlabel('contact scores')
plt.legend()

# Symetric operation for esr1 compounds : 
plt.figure()
top_esr1 = by_esr1[:1000]
sns.distplot(top_esr1['cxcr4'], label = 'cxcr4 score')
sns.distplot(top_esr1['ampc'], label = 'ampc score')
sns.distplot(top_esr1['esr1'], label = 'esr1 score')
sns.distplot(top_esr1['gcr'], label = 'gcr score')
plt.title('1k ESR1 top-scored compounds')
plt.xlabel('contact scores')
plt.legend()


# For akt1 (only some scores available )

plt.figure()
akt1= df['akt1'].dropna()
by_akt1 = df.sort_values(by = 'akt1')

top_akt1 = by_akt1[:1000]
sns.distplot(top_akt1['esr1'], label = 'esr1 score')
sns.distplot(top_akt1['cxcr4'], label = 'cxcr4 score')
sns.distplot(top_akt1['ampc'], label = 'ampc score')
sns.distplot(top_akt1['akt1'], label = 'akt1 score')
plt.title('1k AKT1 top-scored compounds')
plt.xlabel('contact scores')
plt.legend()

