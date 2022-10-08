import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import sys

#Specifying the columns that are important for analysis

columns = ['Participant Private ID', 
           'counterbalance-bkn3',
           'Spreadsheet Name',
           'Reaction Time',
           'Zone Type',
           'Response',
           'blocktype',
           'qtype']

# Preparing variables for Lopp - to find all csv files that contain the our data
# and save it in a list - my_list
the_range = [*range(1,4)]
my_list = []


path = "participant_data\*\**.csv"
    
for fname in glob.glob(path):
   if "6bm9" in fname:
       current_file = pd.read_csv(fname)
       temp_columns = columns.copy()
       temp_columns.append(current_file.loc[0]['counterbalance-bkn3'])
       current_file = current_file[temp_columns]
       current_file.columns = [*current_file.columns[:-1], 'video']         
       my_list.append(current_file)
   temp_columns = []


## Merge all csv files together in one dataframe called final_data
final_data = pd.concat(my_list)


#for the rows, delete all exept those where the value in column "zone type" 
#is response_slider_endValue
final_data = final_data[final_data['Zone Type'].isin(['response_slider_endValue',                                                      'content_video'])]
final_data['video'].fillna(method='ffill', inplace=True) # fill in missing values based on column 'video'
final_data = final_data[final_data['Zone Type'] == 'response_slider_endValue']

# Change question numbers to names

questions_dict = {1: 'positive',
                  2: 'negative',
                  3: 'hunger',
                  4: 'disgust',
                  5: 'awake',
                  6: 'bored',
                  7: 'like'}

final_data["qtype"].replace(questions_dict, inplace=True)

#Wite a csv file called final_data
final_data.to_csv('final_data.csv')

#Creating a Table for plotting
group_category = final_data[['Response', 'blocktype', 'qtype']]
group_category = group_category.astype({'Response':'float'})


#transform table to Pivot table ready for plotting
group_mean = group_category.groupby(['qtype', 'blocktype'])['Response'].mean().unstack()
group_std = group_category.groupby(['qtype', 'blocktype'])['Response'].std().unstack()
group_serr = group_category.groupby(['qtype', 'blocktype'])['Response'].sem().unstack()


group_mean.rename(columns={'D': 'D_mean', 'H': 'H_mean',
                           'N': 'N_mean', 'NU': 'NU_mean', 'P': 'P_mean'}, inplace=True)
group_std.rename(columns={'D': 'D_std', 'H': 'H_std',
                           'N': 'N_std', 'NU': 'NU_std', 'P': 'P_std'}, inplace=True)
group_serr.rename(columns={'D': 'D_serr', 'H': 'H_serr',
                           'N': 'N_serr', 'NU': 'NU_serr', 'P': 'P_serr'}, inplace=True)


mean_std = pd.merge(group_mean, group_std, on='qtype')
category_analysis = pd.merge(mean_std, group_serr, on='qtype')

category_analysis = category_analysis.reindex(['positive', 'negative', 'hunger',
                         'disgust', 'awake', 'bored', 'like'])


#Wite a csv file called final_data
category_analysis.to_csv('category_analysis.csv')


# Plotting the Pivot table to bars
title1 = 'Group Means per Category for each question!'
perr = category_analysis["P_serr"].to_list()
nerr = category_analysis["N_serr"].to_list()
nuerr = category_analysis["NU_serr"].to_list()
herr = category_analysis["H_serr"].to_list()
derr = category_analysis["D_serr"].to_list()

fig, axes = plt.subplots(nrows=5, ncols=1, figsize = (10,30))
fig.suptitle(title1, y = 1)
category_analysis[["P_mean"]].plot(ax=axes[0], kind='bar', rot=0, yerr=perr);
category_analysis[["N_mean"]].plot(ax=axes[1], kind='bar', rot=0, yerr=nerr);
category_analysis[["NU_mean"]].plot(ax=axes[2], kind='bar', rot=0, yerr=nuerr)
category_analysis[["H_mean"]].plot(ax=axes[3], kind='bar', rot=0, yerr=herr);
category_analysis[["D_mean"]].plot(ax=axes[4], kind='bar', rot=0, yerr=derr);
fig.tight_layout()


