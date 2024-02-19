import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import tensorflow as tf
from sklearn.preprocessing import *

model = tf.keras.models.load_model("C:\\Users\\amith\\Documents\\GitHub\\udemy\\Detecting Stress Levels from PPG Sensor Data using Neural Networks\\ML_Model\\model.h5",compile=False)
sc = joblib.load("C:\\Users\\amith\\Documents\\GitHub\\udemy\\Detecting Stress Levels from PPG Sensor Data using Neural Networks\\ML_Model\\scaler.joblib")

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

def predict(ent):
    X = sc.transform(np.array(ent).reshape(1,-1))
    y_pred = model.predict(X)
    return y_pred