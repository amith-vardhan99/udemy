import keras
import numpy as np
from matplotlib.pyplot import imshow
import cv2


base = "C:\\Users\\amith\\Documents\\GitHub\\udemy\\8 - Detecting DeepFakes with ResNet and CNN\\app"
model = keras.models.load_model(f'{base}\\deepfake.h5')

def image_pre(path):
    data = np.ndarray(shape=(1,64,64,1), dtype=np.float32)
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img,(64,64))
    img = np.array(img)
    data = img.reshape((-1,64,64,1))
    return data

def predict(data):
    prediction = model.predict(data)
    return np.round(prediction[0][0])
