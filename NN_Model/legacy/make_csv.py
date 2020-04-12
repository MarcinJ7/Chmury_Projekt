"""
Prepare the csv file for data preprocessing

@author: Malwina
"""

import numpy as np
from scipy.io import loadmat
import pandas as pd
import datetime as date
from dateutil.relativedelta import relativedelta

# params
path_dir = r'D:\chmury\imdb'


cols = ['age', 'gender', 'path', 'face_score1', 'face_score2']

wiki_mat = path_dir + 'imdb.mat'
wiki_data = loadmat(wiki_mat)

del wiki_mat

wiki = wiki_data['imdb']

wiki_photo_taken = wiki[0][0][1][0]
wiki_full_path = wiki[0][0][2][0]
wiki_gender = wiki[0][0][3][0]
wiki_face_score1 = wiki[0][0][6][0]
wiki_face_score2 = wiki[0][0][7][0]

wiki_path = []

for path in wiki_full_path:
    wiki_path.append(path[0])

wiki_genders = []

for n in range(len(wiki_gender)):
    if wiki_gender[n] == 1:
        wiki_genders.append('male')
    else:
        wiki_genders.append('female')

wiki_dob = []

wiki_age = []

for file in wiki_path:
    d1 = file.split('_')[2]
    d1 = d1.split('-')[0]
    d2 = file.split('_')[-1][:-4]
    diff = int(d2) - int(d1)
    wiki_age.append(diff)

final_wiki = np.vstack((wiki_age, wiki_genders, wiki_path, wiki_face_score1, wiki_face_score2)).T

final_wiki_df = pd.DataFrame(final_wiki)

final_wiki_df.columns = cols

meta = final_wiki_df

meta = meta.drop(['face_score1', 'face_score2'], axis=1)
cond = meta[meta['age'] == '-1'].index
meta.drop(cond, inplace=True)

print(meta)

meta = meta.sample(frac=1)

meta.to_csv(path_dir + 'meta.csv', index=False)

print('\n\nWriting to csv file done')