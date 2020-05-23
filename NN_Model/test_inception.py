# Test
import cv2
from tensorflow.keras.models import model_from_json
import matplotlib.pyplot as plt
import numpy as np

tar_size = 299
path_dir = r'D:/chmury/imdb/preprocessed/'            # path of preprocessed images

# Wczytanie modelu
json_file = open(path_dir + 'model_inc.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(path_dir + 'model_inc.h5')
print('Loaded model from disk')

# Test
image = cv2.imread(path_dir + '02/nm0000002_rm454874624_1924-9-16_1991.jpg')
image = cv2.resize(image, (tar_size, tar_size))
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# b,g,r = cv2.split(image)        # opencv ma format BGR, więc trzeba przekształcić na RGB
# image2 = cv2.merge([r,g,b])
plt.imshow(image)
plt.axis("off")
plt.show()

X = np.expand_dims(image, axis=[0])
y_pred = model.predict(X)[0][0]
print('Wiek: ', y_pred)

image = cv2.imread(path_dir + '03/nm0000403_rm801150976_1964-1-27_2003.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (tar_size, tar_size))
# b,g,r = cv2.split(image)        # opencv ma format BGR, więc trzeba przekształcić na RGB
# image2 = cv2.merge([r,g,b])
plt.imshow(image)
plt.axis("off")
plt.show()

X = np.expand_dims(image, axis=[0])
y_pred = model.predict(X)[0][0]
print('Wiek: ', y_pred)