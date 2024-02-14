import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
from datetime import *

model = tf.keras.models.load_model("model.keras")
mms = joblib.load("scaler.joblib")

cont = np.load("closing price window and target.npz")

X = cont["window"]
y = cont["target"]
length = cont["window_size"]

X_train_val = mms.fit_transform(X)
y_train_val = mms.fit_transform(y.reshape(-1,1))

train_val_threshold = round(0.8 * X.shape[0])
length_of_window = length

X_train = X_train_val[:train_val_threshold]
y_train = y_train_val[:train_val_threshold]

X_val = X_train_val[train_val_threshold:]
y_val = y_train_val[train_val_threshold:]

train_rows =  X_train.shape[0]
val_rows = X_val.shape[0]

X_train = X_train.reshape(train_rows, 1, length_of_window)
X_val = X_val.reshape(val_rows, 1, length_of_window)

model.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.mean_squared_error)
model.fit(X_train, y_train, validation_data = (X_val, y_val), epochs=100, batch_size=32, verbose=1, shuffle=True, callbacks=tf.keras.callbacks.EarlyStopping(patience=2))

def generate_dates(future_end_date):
    future_start_date = "2020-04-16 01:00:00"
    future_end_date = future_end_date.strip()
    future_end_date = pd.to_datetime(future_end_date+" 01:00:00")

    future_dates = pd.date_range(start=future_start_date,end=future_end_date,freq="h").values
    return future_dates

def generate_future_targets(future_dates):

    X_test = []
    y_test = []

    input_arr = np.array(X_train_val[-1,1:].tolist() + [y_train_val[-1][0]])
    output = model.predict(input_arr.reshape(1,1,-1),verbose=0)[0][0]
    X_test.append(input_arr)
    y_test.append(output)
    i = 0

    for i in range(1,len(future_dates)):
        current_window = X_test[i-1]
        input_arr = np.array(current_window[1:].tolist() + [y_test[i-1]])
        output = model.predict(input_arr.reshape(1,1,-1))[0][0]
        X_test.append(input_arr)
        y_test.append(output)

    X_test = np.array(X_test)
    y_test = np.array(y_test)

    y_pred = mms.inverse_transform(y_test.reshape(-1,1))

    return y_pred