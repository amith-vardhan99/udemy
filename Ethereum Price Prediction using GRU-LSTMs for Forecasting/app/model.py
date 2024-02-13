import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
from datetime import *

model = tf.keras.models.load_model("model.joblib")
mms = joblib.load("scaler.joblib")

no_of_window_samples = 240

