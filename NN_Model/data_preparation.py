"""
Preparation of data: face detection, cropping images and making a csv file

@author: Malwina
"""
import os
from scipy.io import loadmat
import cv2
import csv

# params
path_input = r'D:/chmury/imdb/imdb_crop/imdb_crop/'      # path of the dataset
path_output = r'D:/chmury/imdb/preprocessed/'            # path of preprocessed images

# path of the haar cascade classifier
path_classifier = r'C:/Users/cp/Documents/GitHub/Chmury_Projekt/Face_Detection/haarcascade_frontalface_default.xml'
target_size = (299, 299)

face_cascade = cv2.CascadeClassifier(path_classifier)

if not os.path.exists(path_output):
    os.makedirs(path_output)

path_mat = path_input + r'/imdb.mat'
mat_data = loadmat(path_mat)
mat_data = mat_data['imdb']

mat_paths = mat_data[0][0][2][0]
mat_gender = mat_data[0][0][3][0]

# tables of csv files to train and test network
output_train = [['path', 'age', 'gender']]
output_test = [['path', 'age', 'gender']]

i = 0
j = -1
for path in mat_paths:
    path = str(path[0])
    path_new = path_input + path
    image = cv2.imread(path_new)
    j += 1
    if type(image) == 'NoneType':
        continue
    path_save = path_output + str(i) + '.jpg'
    row = []

    # age calculation
    d1 = path.split('_')[2]
    d1 = d1.split('-')[0]
    d2 = path.split('_')[-1][:-4]
    age = int(d2) - int(d1)

    # face detection (@Marcin)
    faces = face_cascade.detectMultiScale(image, 1.3, 5)
    for (x, y, w, h), k in zip(faces, list(range(len(faces)))):
        crop_img = image[y:y + h, x:x + w]
        crop_img = cv2.resize(crop_img, target_size)
        cv2.imwrite(path_save, crop_img)
        break

    row.append(path_save)
    row.append(age)
    row.append(mat_gender[j])

    # 20% of data (1/5) will be saved to test file
    if i % 5 == 0:
        output_test.append(row)
    else:
        output_train.append(row)
    i += 1

print('Preprocessed', i, 'images')
print('Number of training photos:', len(output_train))
print('Number of testing photos:', len(output_test))

# save csv files
path_file = path_output + 'dataset_train.csv'
with open(path_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_train)

path_file = path_output + 'dataset_test.csv'
with open(path_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_test)

print('Saved files')
