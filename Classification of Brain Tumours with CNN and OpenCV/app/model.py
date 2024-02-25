import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import cv2
import warnings
warnings.filterwarnings("ignore")
import shutil
from sklearn.metrics import *
import cv2

model = tf.keras.models.load_model("model.h5")
def image_preprocessing(img_path):
    img_org = cv2.imread(img_path)
    img_grey = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(src=img_grey, dsize=(128,128))
    img = img / 255.0
    img = img.reshape((1,128,128,1))
    return img

def predict_result(img):
    pred = int(model.predict(img,verbose=0)[0][0])
    return pred