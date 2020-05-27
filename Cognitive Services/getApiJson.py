# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:49:12 2020

@author: Marcin
"""

import requests
import json
import cv2 
import numpy as np
from urllib.request import urlopen

subscription_key = '883d7...0'

face_api_url = 'https://comparetomodelapi.cognitiveservices.azure.com/face/v1.0/detect'

image_url = 'https://victoria.mediaplanet.com/app/uploads/sites/103/2019/04/Main-11.jpg'

req = urlopen(image_url)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)

headers = {'Ocp-Apim-Subscription-Key': subscription_key}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})

x  = response.json()

# Wiek:
for i in x:
    print("Wykryto osobe, wiek: " + str(i["faceAttributes"]["age"]))
    face_rect = i["faceRectangle"]
    img = cv2.rectangle(img,(face_rect['left'],face_rect['top']),(face_rect['left']+face_rect['width'],face_rect['top']+face_rect['height']),(122,122,255),2)
    img = cv2.putText(img, ("Wiek: " + str(i["faceAttributes"]["age"])) , (face_rect['left'], face_rect['top']-20) , cv2.FONT_HERSHEY_SIMPLEX, 1, (100,100,255) , 2 , cv2.LINE_AA) 

cv2.imshow("Our Picture", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
