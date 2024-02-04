# import numpy as np
# import pandas as pd
import tensorflow as tf
import os

path = os.getcwd().replace("\\","/")
model = tf.keras.models.load_model(path+"/deep_learning_linear_regression.h5")

#%%
