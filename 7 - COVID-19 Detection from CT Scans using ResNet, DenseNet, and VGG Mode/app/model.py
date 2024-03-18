import keras
import numpy as np
from matplotlib.pyplot import imshow
import cv2


base = 'C:\\Users\\amith\\Documents\\GitHub\\udemy\\7 - COVID-19 Detection from CT Scans using ResNet, DenseNet, and VGG Mode\\app'
model = keras.models.load_model(f'{base}\\CovidTest.h5')

def image_pre(path):
    print(path)
    image = cv2.imread(path)
    image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
    image = cv2.resize(src=image,dsize=(64,64))
    data = image.reshape((64,64,1))
    data = data / 255.0
    return data

def predict(data):
    prediction = model.predict(data.reshape(1,64,64,1))[0][0]
    return np.int64(np.round(prediction))
