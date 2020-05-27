from flask import Flask, request
from tensorflow.keras.models import model_from_json
import cv2
import numpy as np
import requests
import pyodbc

# params
path_model = r'/flask/'       # ścieżka do modelu
path_dir = r'/flask/'         # ścieżka do przerobionych zdjęć
path_classifier = r'/flask/haarcascade_frontalface_default.xml'
target_size = (299, 299)
face_cascade = cv2.CascadeClassifier(path_classifier)
server = r'serwerdb.database.windows.net'
database = r'DB'
username = r'azureuser'
password = r'Password.1!!'


def load_model(model_filename='model_cnn.json', weights_filename='model_cnn.h5'):
    global model
    json_file = open(path_model + model_filename, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(path_model + weights_filename)
    print('Loaded model from disk')


app = Flask(__name__)

# Wczytanie modelu
load_model()

@app.route('/', methods=['POST'])
def predict_age():
    url = request.get_json().get('url')
    resp = requests.get(url, stream=True).raw
    bytes = bytearray(resp.read())
    image = np.asarray(bytes, dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    faces = face_cascade.detectMultiScale(image, 1.3, 5)
    images_list = []
    predictions = []
    driver = r'{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect(
        r'DRIVER=' + driver + r';SERVER=' + server + r';PORT=1433;DATABASE=' + database + r';UID=' + username + r';PWD=' + password)
    cursor = cnxn.cursor()
    for (x, y, w, h), k in zip(faces, list(range(len(faces)))):
        crop_img = image[y:y + h, x:x + w]
        crop_img = cv2.resize(crop_img, target_size)
        images_list.append(crop_img)

    for image in images_list:
        b, g, r = cv2.split(image)  # opencv ma format BGR, więc trzeba przekształcić na RGB
        image = cv2.merge([r / 255, g / 255, b / 255])
        X = np.expand_dims(image, axis=[0])
        y_pred = model.predict(X)[0][0]
        predictions.append(str(int(y_pred)))
        age = int(y_pred)
        cursor.execute("INSERT predicted_age (age, photo) VALUES (?, ?);", (age, bytes))
    cnxn.commit()
    cursor.close()
    cnxn.close()

    return {
        "age": ', '.join(predictions)
    }
