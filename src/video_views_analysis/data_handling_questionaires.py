# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 09:16:48 2022

@author: Angela Lazova
"""

import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import sys


# Preparing variables for Lopp - to find all csv files that contain
# our data within the 7 questionaires and merge them together.

data_dict = {
    'DEMOGRAPHICS_DATA': [],
    'BIG_FIVE_DATA': [],
    'DISGUST_SENS_DATA': [],
    'INTUITIVE_EAT_DATA': [],
    'STAI_DATA': [],
    'PANAS_DATA': [],
    'MAIA_DATA': []  
    }

columns = [
    'Participant Private ID',
    'Question Key',
    'Response'
    ]


path = "E:/Second_lab_rotation/valiaffect/participant_data/*/**.csv"
    
for fname in glob.glob(path):
   if "pk1q" in fname:
       current_file = pd.read_csv(fname)        
       data_dict['DEMOGRAPHICS_DATA'].append(current_file)
   elif "7eyu" in fname:
       current_file = pd.read_csv(fname)        
       data_dict['BIG_FIVE_DATA'].append(current_file)
   elif "eouc" in fname:
       current_file = pd.read_csv(fname)        
       data_dict['DISGUST_SENS_DATA'].append(current_file)
   elif "v7qc" in fname:
       current_file = pd.read_csv(fname)        
       data_dict['INTUITIVE_EAT_DATA'].append(current_file)
   elif "n8ue" in fname:
       current_file = pd.read_csv(fname)        
       data_dict['STAI_DATA'].append(current_file)
   elif "ioia" in fname:
       current_file = pd.read_csv(fname)        
       data_dict['PANAS_DATA'].append(current_file)
   elif "1r1o" in fname:
       current_file = pd.read_csv(fname)        
       data_dict['MAIA_DATA'].append(current_file)

## Merge all csv files together in one dataframe called final_data      
for questionaire, data in data_dict.items():
    current_category_df = pd.concat(data)
    current_category_df.to_csv('data/{}.csv'.format(questionaire))
    
    
    

