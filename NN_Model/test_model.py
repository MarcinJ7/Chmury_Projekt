"""
Test the trained model

@author: Malwina
"""

from tensorflow.keras.models import model_from_json

# Wczytanie modelu
json_file = open(path_dir + 'model_cnn.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(path_dir + 'model_cnn.h5')
print('Loaded model from disk')

# Test
image = cv2.imread(path_dir + 'dataset/test/07/14853007_1984-05-07_2007.jpg')
image = cv2.resize(image, (tar_size, tar_size))
b,g,r = cv2.split(image)        # opencv ma format BGR, więc trzeba przekształcić na RGB
image2 = cv2.merge([r,g,b])
plt.imshow(image, cmap='gray')
plt.axis("off")
plt.show()

X = np.expand_dims(image, axis=[0, 3])
y_pred = model.predict(X)[0][0]
print('Wiek: ', y_pred)

image = cv2.imread(path_dir + 'dataset/test/07/440507_1969-12-10_2014.jpg')
image = cv2.resize(image, (tar_size, tar_size))
b,g,r = cv2.split(image)        # opencv ma format BGR, więc trzeba przekształcić na RGB
image2 = cv2.merge([r,g,b])
plt.imshow(image, cmap='gray')
plt.axis("off")
plt.show()

X = np.expand_dims(image, axis=[0, 3])
y_pred = model.predict(X)[0][0]
print('Wiek: ', y_pred)