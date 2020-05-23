"""
Test the trained model

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

# Wczytanie modelu
load_model()

# Test
predict_age(460682)
predict_age(459951)
predict_age(14)
predict_age(13)
# predict_age(18)
# predict_age(57)
predict_age(355)
# predict_age(351)
# predict_age(460301)
predict_age(460326)
