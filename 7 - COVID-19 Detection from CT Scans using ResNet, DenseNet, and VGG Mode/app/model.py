import keras
import numpy as np
import matplotlib.pyplot as plt
import cv2


path = "C:\\Users\\amith\\Documents\\GitHub\\udemy\\7 - COVID-19 Detection from CT Scans using ResNet, DenseNet, and VGG Mode\\app"
model = keras.models.load_model(f'{path}\\model.h5')

def image_pre(file_name):
    img = cv2.imread(file_name)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_resized = cv2.resize(src=img_grey,dsize=(64,64))
    data = img_resized / 255.0
    data = data.reshape((64,64,1))
    return data

def predict(data):
    prediction = model.predict(data.reshape(1,64,64,1))[0][0]
    return np.int64(np.round(prediction))
