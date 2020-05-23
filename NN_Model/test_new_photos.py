"""
Test the trained model with new photos

@author: Malwina
"""

from tensorflow.keras.models import model_from_json
import cv2
import matplotlib.pyplot as plt
import numpy as np


def load_model(model_filename='model_cnn.json', weights_filename='model_cnn3.h5'):
    global model
    json_file = open(path_model + model_filename, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(path_model + weights_filename)
    print('Loaded model from disk')


def predict_age(filename):
    filename = str(filename) + '.jpg'
    image = cv2.imread(path_dir + filename)
    faces = face_cascade.detectMultiScale(image, 1.3, 5)
    images_list = []
    for (x, y, w, h), k in zip(faces, list(range(len(faces)))):
        crop_img = image[y:y + h, x:x + w]
        crop_img = cv2.resize(crop_img, target_size)
        images_list.append(crop_img)

    for image in images_list:
        b, g, r = cv2.split(image)                      # opencv ma format BGR, więc trzeba przekształcić na RGB
        image = cv2.merge([r / 255, g / 255, b / 255])
        X = np.expand_dims(image, axis=[0])
        y_pred = model.predict(X)[0][0]
        print('Wiek: ', int(y_pred))
        plt.imshow(image, cmap='gray')
        plt.axis("off")
        plt.show()


path_model = r'D:/repo/age-detection-on-azure/NN_Model/models/'      # ścieżka do modelu
path_dir = r'D:/chmury/imdb/preprocessed/'                          # ścieżka do przerobionych zdjęć
# path_dir = r'D:/chmury/imdb/test/'
path_classifier = r'C:/Users/cp/Documents/GitHub/Chmury_Projekt/Face_Detection/haarcascade_frontalface_default.xml'
target_size = (299, 299)
face_cascade = cv2.CascadeClassifier(path_classifier)

# Wczytanie modelu
load_model()

# Test
files = [460682, 459951, 14, 13, 18, 57, 355, 351, 460301, 460326]
for file in files:
    predict_age(file)
