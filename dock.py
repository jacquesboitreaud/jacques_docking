# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 18:20:49 2019

@author: jacqu
"""
from main_np import cline
import pandas as pd 

parser = argparse.ArgumentParser()
df = pd.read_csv('/home/mcb/jboitr/data/moses_test.csv', nrows = 100)

smiles = df['can']

main(smiles = smiles)

