import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import tensorflow as tf
from sklearn.preprocessing import *

model = tf.keras.models.load_model("model.h5",compile=False)
sc = joblib.load("scaler.joblib")

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

def predict(ent):
    X = sc.transform(ent)
    y_pred = model.predict(X)
    return y_pred