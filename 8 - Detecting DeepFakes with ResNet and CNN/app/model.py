import keras
import numpy as np
from matplotlib.pyplot import imshow
import cv2


base = '/Users/adityavs14/Documents/Internship/Pianalytix/Deep_Fake/app'
model = keras.models.load_model(f'{base}/deepfake.h5')

def image_pre(path):
    data = np.ndarray(shape=(1,128,128, 1), dtype=np.float32)
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img,(128, 128))
    img = np.array(img)
    data = img.reshape((-1,128,128,1))
    return data

def predict(data):
    prediction = model.predict(data)
    return np.round(prediction[0][0])
