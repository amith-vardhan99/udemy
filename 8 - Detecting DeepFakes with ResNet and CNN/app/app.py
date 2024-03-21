from flask import Flask, render_template, request
import numpy as np
import os
from model import image_pre,predict
#import seaborn as sns
#import matplotlib.pyplot as plt
#import pandas as pd

app = Flask(__name__)


UPLOAD_FOLDER = '/Users/adityavs14/Documents/Internship/Pianalytix/Deep_Fake/app/static'
ALLOWED_EXTENSIONS = set(['jpg'])
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
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.jpg')
        file1.save(path)
        data = image_pre(path)
        s = predict(data)
        if s == 1:
            result = 'Real face'
        else:
            result = 'Fake face'
    return render_template('index.html',result=result) 





if __name__ == "__main__":
    app.run(debug=True)