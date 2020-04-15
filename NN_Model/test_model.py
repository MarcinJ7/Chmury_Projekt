"""
Test the trained model

@author: Malwina
"""

from tensorflow.keras.models import model_from_json
import cv2
import matplotlib.pyplot as plt
import numpy as np

path_dir = r'D:/chmury/imdb/preprocessed/'            # path of preprocessed images

# Wczytanie modelu
json_file = open(path_dir + 'model_cnn.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(path_dir + 'model_cnn.h5')
print('Loaded model from disk')

# Test
image = cv2.imread(path_dir + '460682.jpg')
b, g, r = cv2.split(image)        # opencv ma format BGR, więc trzeba przekształcić na RGB
image = cv2.merge([r / 255, g / 255, b / 255])
plt.imshow(image, cmap='gray')
plt.axis("off")
plt.show()

X = np.expand_dims(image, axis=[0])
y_pred = model.predict(X)[0][0]
print('Wiek: ', y_pred)

image = cv2.imread(path_dir + '459951.jpg')
b, g, r = cv2.split(image)        # opencv ma format BGR, więc trzeba przekształcić na RGB
image = cv2.merge([r / 255, g / 255, b / 255])
plt.imshow(image)
plt.axis("off")
plt.show()

X = np.expand_dims(image, axis=[0])
y_pred = model.predict(X)[0][0]
print('Wiek: ', y_pred)