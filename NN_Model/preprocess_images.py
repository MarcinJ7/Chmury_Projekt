"""
Prepare the images

@author: Malwina
"""

import cv2
import os
from sklearn.model_selection import train_test_split
import csv
import pandas as pd

# params
path_dir = r'D:\chmury\imdb'

# Załadowanie pliku csv
meta = pd.read_csv(path_dir + 'meta.csv')
meta = meta.drop(['gender'], axis=1)
meta = meta.values

# Podział na dane trenignowe i walidacyjne
D_train, D_test = train_test_split(meta, test_size=0.2, random_state=42)
print('Found', len(D_train), 'learning photos and', len(D_test), 'testing photos in csv file')

# Nowe pliki csv
cols = ['filepath', 'age']
train_csv = [cols]
test_csv = [cols]

# Utworzenie folderów
dataset_train_path = path_dir + 'dataset/train/'
for i in range(5):
    output_dir_train = dataset_train_path + '0' + str(i)
    if not os.path.exists(output_dir_train):
        os.makedirs(output_dir_train)

dataset_test_path = path_dir + 'dataset/test/'
for i in range(5):
    output_dir_test = dataset_test_path + '0' + str(i)
    if not os.path.exists(output_dir_test):
        os.makedirs(output_dir_test)

# Przerobienie zdjęć i zapis do nowych plików csv
counter = 0
for image in D_train:
    img_path = path_dir + image[1]
    img = cv2.imread(img_path, 1)
    if type(img) == 'NoneType':
      continue
    # try:
    #   img = cv2.resize(img, (256, 256))
    #   img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # except:
    #   continue
    # path_to_write = dataset_train_path + image[1]
    # try:
    #     cv2.imwrite(path_to_write, img)
    # except:
    #     continue
    counter += 1
    path_to_write = img_path
    line = [path_to_write, image[0]]
    train_csv.append(line)
print('Processed', counter, 'training photos')

counter = 0
for image in D_test:
    img_path = path_dir + image[1]
    img = cv2.imread(img_path, 1)
    if type(img) == 'NoneType':
        continue
    # try:
    #   img = cv2.resize(img, (256, 256))
    #   img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # except:
    #   continue
    # path_to_write = dataset_test_path + image[1]
    # try:
    #     cv2.imwrite(path_to_write, img)
    # except:
    #     continue
    counter += 1
    path_to_write = img_path
    line = [path_to_write, image[0]]
    test_csv.append(line)
print('Processed', counter, 'testing photos')

# Zapis plików csv
with open(path_dir + 'train.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(train_csv)

with open(path_dir + 'test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(test_csv)

print('Done')