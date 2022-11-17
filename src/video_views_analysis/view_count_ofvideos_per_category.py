# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 09:56:57 2022

@author: Angela Lazova
"""

import pandas as pd

complete_file = pd.read_csv('all_videos.csv')

positive = complete_file.iloc[:,[0,1,2,3,4]]  # anotger way to split pos = complete_file[['P', 'P.1']]
negative = complete_file.iloc[:,[5,6,7,8,9]]
neutral = complete_file.iloc[:,[10,11,12,13,14]]
hunger = complete_file.iloc[:,[15,16,17,18,19]]
disgust = complete_file.iloc[:,[20,21,22,23,24]]

# counting how many times each video in each category is viewed and
# adding a new column in each dataframe from the sum of views
positive_views = positive.apply(pd.value_counts)
positive_views['P_views'] = positive_views.sum(axis=1)

negative_views = negative.apply(pd.value_counts)
negative_views['N_views'] = negative_views.sum(axis=1)

neutral_views = neutral.apply(pd.value_counts)
neutral_views['NU_views'] = neutral_views.sum(axis=1)

hunger_views = hunger.apply(pd.value_counts)
hunger_views['H_views'] = hunger_views.sum(axis=1)

disgust_views = disgust.apply(pd.value_counts)
disgust_views['D_views'] = disgust_views.sum(axis=1)

views_table = pd.concat([positive_views['P_views'], 
                         negative_views['N_views'],
                         neutral_views['NU_views'],
                         hunger_views['H_views'],
                         disgust_views['D_views']], axis=1, keys=['P_views', 
                                                                  'N_views',
                                                                  'NU_views',
                                                                  'H_views',
                                                                  'D_views'])
views_table.to_csv('views_table.csv')

