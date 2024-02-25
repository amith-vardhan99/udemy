from flask import *
import numpy as np
import os
from model import *
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)


UPLOAD_FOLDER = "C:\\Users\\amith\\Documents\\GitHub\\udemy\\Classification of Brain Tumours with CNN and OpenCV\\app\\static"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.jpg')
        file1.save(path)
        #return path
        data = image_preprocessing(path)
        s = predict_result(data)
        if s == 1:
            result = 'Brain Tumour is not present'
        else:
            result = 'Brain Tumour is present'
    return render_template('index.html',result=result)


if __name__ == "__main__":
    app.run(debug=True)