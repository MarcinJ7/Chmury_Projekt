"""
Script for fixing the csv files (checking if the image exists)

author: @Malwina
"""

import csv
import os

# params
path_train_input = r'D:/chmury/imdb/preprocessed/dataset_train.csv'            # path of preprocessed images
path_train_output = r'D:/chmury/imdb/preprocessed/train.csv'            # path of preprocessed images
path_test_input = r'D:/chmury/imdb/preprocessed/dataset_test.csv'            # path of preprocessed images
path_test_output = r'D:/chmury/imdb/preprocessed/test.csv'            # path of preprocessed images

output_train = []
output_test = []

# train images
with open(path_train_input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    j = 1
    for row in reader:
        if i == 0:
            output_train.append(row)
            i += 1
            continue
        if len(row) == 0:
            continue
        path_image = row[0]
        age = row[1]
        gender = row[2]
        i += 1

        # check if image exists -> if age is positive -> if gender is not nan
        if os.path.isfile(path_image):
            if int(age) > 0:
                if gender != 'nan':
                    output_train.append(row)
                    j += 1

# new train file
with open(path_train_output, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_train)

print('Train file: processed', i, 'rows, deleted', i-j)

# test images
with open(path_test_input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    j = 1
    for row in reader:
        if i == 0:
            output_test.append(row)
            i += 1
            continue
        if len(row) == 0:
            continue
        path_image = row[0]
        age = row[1]
        gender = row[2]
        i += 1

        # check if image exists -> if age is positive -> if gender is not nan
        if os.path.isfile(path_image):
            if int(age) > 0:
                if gender != 'nan':
                    output_test.append(row)
                    j += 1

# new test file
with open(path_test_output, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_test)

print('Train file: processed', i, 'rows, deleted', i-j)
print('Number of images:', len(output_train) + len(output_test))


