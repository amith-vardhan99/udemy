from flask import Flask, render_template, request
import numpy as np
import os
from model import image_pre,predict
import cv2
import matplotlib.pyplot as plt
#import seaborn as sns
#import matplotlib.pyplot as plt
#import pandas as pd

app = Flask(__name__)


UPLOAD_FOLDER = 'C:\\Users\\amith\\Documents\\GitHub\\udemy\\10 - Land Segmentation using U-Net Architecture\\app\\static'
base = "C:\\Users\\amith\\Documents\\GitHub\\udemy\\10 - Land Segmentation using U-Net Architecture\\app"
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
        plt.switch_backend('Agg') 
        data = image_pre(path)
        s = predict(data)
        #filter = np.array([[-1, -1, -1], [-1, 16, -1], [-1, -1, -1]]) 
        #imgSharpen = cv2.filter2D(s,-1,filter)
        imgSharpen = s
        #print('\n\n',imgSharpen,'\n\n')
        plt.imshow(imgSharpen)
        plt.savefig(f'{base}\\static\\output.png')
    return render_template('index.html') 





if __name__ == "__main__":
    app.run(debug=True)