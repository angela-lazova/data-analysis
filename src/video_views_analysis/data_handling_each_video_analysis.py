# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:28:01 2022

@author: Angela Lazova
"""
import pandas as pd

#Improting the data file
video_data = pd.read_csv('data/PARTICIPANTS_DATA.csv')
video_data = video_data.sort_values('video')


#Counting how many times each video is seen
#for the rows, delete all exept those where the value in column "qtype" is positive (randomly taking one question to prevent counting one video view twice)
views = video_data[video_data['qtype'].isin(['positive'])] #since each video view is written times 7 - onvce for each question, and we want to count it only as one view, we delete the other 6 times it is written
        

P = views[views['blocktype'].isin(['P'])]
P_views = P['video'].value_counts().rename_axis('videos').reset_index(name='counts')

N = views[views['blocktype'].isin(['N'])]
N_views = N['video'].value_counts().rename_axis('videos').reset_index(name='counts')

NU = views[views['blocktype'].isin(['NU'])]
NU_views = NU['video'].value_counts().rename_axis('videos').reset_index(name='counts')

H = views[views['blocktype'].isin(['H'])]
H_views = H['video'].value_counts().rename_axis('videos').reset_index(name='counts')

D = views[views['blocktype'].isin(['D'])]
D_views = D['video'].value_counts().rename_axis('videos').reset_index(name='counts')

list_of_views = [P_views, N_views, NU_views, H_views, D_views]
all_views = pd.concat(list_of_views)
all_views = all_views.sort_values('videos')
all_views.rename(columns={"videos": "video"}, inplace=True)
all_views.to_csv('all_views.csv')


# Specifying columns of interest
columns = [
    'video',
    'Response',
    'blocktype',
    'qtype'
    ]

complete_views_data = video_data[columns]
trying1 = complete_views_data.to_csv('plotting_videos.csv')


video_means = complete_views_data.groupby(['video', 'qtype'])['Response'].mean().unstack()
trying = video_means.to_csv('data/VIDEO_MEANS.csv')


# Preparing csv files for plotting

# Creating dictionairies to loop through

categories = ['P','N','NU','H','D']
category_dict = {key:value for (key, value) in zip(range(len(categories)), categories)}

questions = ['positive','negative','hunger','disgust','awake','bored','like']
question_dict = {key:value for (key, value) in zip(range(len(questions)), questions)}

#Looping through dictionaires and creating files
for category_value in category_dict.values():
    temp_file = video_data[video_data['blocktype'].isin([category_value])]
    for question_value in question_dict.values():
        plotting_file = temp_file[temp_file['qtype'].isin([question_value])]
        plotting_file = pd.merge(plotting_file, all_views, on="video")
        plotting_file.to_csv('plotting_files/{}_{}_videos.csv'.format(category_value, question_value))
