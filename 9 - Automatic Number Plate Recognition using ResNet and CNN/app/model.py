from tensorflow import keras
import numpy as np
from matplotlib.pyplot import imshow
import cv2
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import plotly.express as px


base = 'C:\\Users\\amith\\Documents\\GitHub\\udemy\\9 - Automatic Number Plate Recognition using ResNet and CNN\\app'
model = keras.models.load_model(f'{base}\\NPD.h5')

def image_pre(path):
    #print(path)
    img_org = cv2.imread(path)
    height,width,depth = img_org.shape
    img_resized = cv2.resize(src=img_org,dsize=(128,128))
    img_reshaped = img_resized / 255.0

    X = np.array(img_reshaped,dtype=np.float64).reshape(-1,128,128,3)
    return X,width,height
    
    #img_arr = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    #h,w,d = img_arr.shape
    #load_image = load_img(path,target_size=(128,128))
    #load_image_arr = img_to_array(load_image)
    #norm_load_image_arr = load_image_arr/255.0
    #X = np.array(norm_load_image_arr,dtype=np.float64).reshape(-1,128,128,3)
    #return X,w,h

def predict(data,width,height):
    prediction = model.predict(data)
    xmin = prediction[0][0] * width
    xmax = prediction[0][1] * width
    ymin = prediction[0][2] * height
    ymax = prediction[0][3] * height
    return xmin,xmax,ymin,ymax
