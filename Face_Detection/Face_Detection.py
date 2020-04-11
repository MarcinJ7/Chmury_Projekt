# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 17:32:35 2020

@author: Marcin
"""

# Przykład wykrywania twarzy z gotowym wytrenowanym klasyfikatorem Haara
# LINK do klasyfikatora: https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades_cuda/haarcascade_frontalface_default.xml
import cv2 

# params
target_size = (299, 299)
path_classifier = r'C:\Users\Marcin\Desktop\haarcascade_frontalface_default.xml'
path_image = r'C:\Users\Marcin\Desktop\faces.jpg'

# Podajemy tutaj sciezke do klasyfikatora (*.xml)
face_cascade = cv2.CascadeClassifier(path_classifier)

# Tutaj można dać pętle po wszystkich obrazach w katalogu
# Roboczo tylko dla jednego obrazu -> scieżka, wczytanie obrazu
img = cv2.imread(path_image)
# Konwersja na skalę szarości
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Wyszukanie twarzy na obrazie
faces = face_cascade.detectMultiScale(img, 1.3, 5)

# Zapis kazdej ze znalezionych twarzy do pliku, zmiana rozmiaru na taki,
# ktory jest w sieci neuronowej u @Malwina, pokazanie obrazu powstałego
# Przewijamy jakimkolwiek klawiszem
for (x, y, w, h), k in zip(faces, list(range(len(faces)))):
    # img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    crop_img = img[y:y+h, x:x+w]
    crop_img = cv2.resize(crop_img, target_size)
    cv2.imshow("cropped", crop_img)
    cv2.imwrite((str(k) + "jakas_nazwa.jpg"), crop_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
