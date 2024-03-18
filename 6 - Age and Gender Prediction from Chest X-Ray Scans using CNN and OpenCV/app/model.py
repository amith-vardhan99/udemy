import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import opendatasets as od
import tensorflow as tf
import cv2
from tqdm import *

base = 'C:\\Users\\amith\\Documents\\GitHub\\udemy\\6 - Age and Gender Prediction from Chest X-Ray Scans using CNN and OpenCV\\app'
model_genders = tf.keras.models.load_model("C:\\Users\\amith\\Documents\\Datasets\\model_genders.h5")
model_ages = tf.keras.models.load_model("C:\\Users\\amith\\Documents\\Datasets\\model_ages.h5")

def image_preprocess(path):
    data = np.ndarray(shape=(1,64,64,1), dtype=np.float32)
    img_org = cv2.imread(f'{base}\\static\\input.png')
    img_gray = cv2.cvtColor(src=img_org, code=cv2.COLOR_BGR2GRAY)
    img_short = cv2.resize(src=img_gray, dsize=(64,64))
    img = img_short / 255.0
    data = img.reshape((1,64,64,1))
    return data

def image_predict(data):
    pred_ages = model_ages.predict(data)
    pred_genders = model_genders.predict(data)
    return pred_ages, pred_genders
