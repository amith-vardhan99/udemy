import keras
import numpy as np
import matplotlib.pyplot as plt
import cv2


shape = (64,64)
base = 'C:\\Users\\amith\\Documents\\GitHub\\udemy\\10 - Land Segmentation using U-Net Architecture\\app'
model = keras.models.load_model(f'{base}\\TerrainMaskGenerator.h5')

def image_pre(path):
    #print(path)
    data = plt.imread(path)
    data = cv2.resize(data, shape)
    data = np.array(data).reshape(1,64,64,3)
    #print(data.shape)
    return data

def predict(data):
    print('\n\n',data.shape,'\n\n')
    predictions = model.predict(data)
    predictions= cv2.merge((predictions[0,:,:,0],predictions[0,:,:,1],predictions[0,:,:,2]))
    return predictions


