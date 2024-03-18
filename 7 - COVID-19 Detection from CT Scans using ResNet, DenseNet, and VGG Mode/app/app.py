from flask import Flask, render_template, request
import numpy as np
import os
from model import image_pre,predict
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)


UPLOAD_FOLDER = 'C:\\Users\\amith\\Documents\\GitHub\\udemy\\7 - COVID-19 Detection from CT Scans using ResNet, DenseNet, and VGG Mode\\app\\static\\'

ALLOWED_EXTENSIONS = set(['png'])
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
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.png')
        file1.save(path)
        data = image_pre(path)
        s = predict(data)
        if s == 1:
            result = 'No COVID detected'
        else:
            result = 'COVID detected'
    return render_template('index.html',result=result) 





if __name__ == "__main__":
    app.run(debug=True)