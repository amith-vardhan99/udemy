import numpy as np
import tensorflow as tf
import os
import joblib

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def predict_total_sale_price(vals):

    path = os.getcwd().replace("\\","/")
    list_of = ""
    with open("list_of_features.txt","r+") as fl:
        list_of = fl.read()
    list_of = list_of.split("\n")
    list_of_features = list_of[0].split(", ")
    list_of_dtypes = list_of[1].split(", ")

    vals = vals.reshape(-1,1)
    final_out = []
    ctr = 0
    for i in vals:
        if list_of_dtypes[ctr] == "object":
            file_name = path + "/" + list_of_features[ctr] + ".joblib"
            label_encoder_model = joblib.load(file_name)
            lt = float(label_encoder_model.transform(i)[0])
            final_out.append(lt)
            print(lt)
        else:
            final_out.append(float(i[0]))
        ctr += 1
    final_out = np.array(final_out).reshape(1,-1)

    path = os.getcwd().replace("\\","/") + "/deep_learning_linear_regression.h5"
    model = tf.keras.models.load_model(path)
    model.compile(optimizer=tf.keras.optimizers.Adam(),loss=tf.keras.losses.mean_squared_error,metrics=tf.keras.metrics.mean_absolute_error)

    final_prediction = abs(model.predict(final_out)[0][0])

    return final_prediction
#%%

#%%
