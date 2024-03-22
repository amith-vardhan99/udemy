from flask import Flask, render_template, request
import numpy as np
import os
from model import image_pre,predict
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import cv2



app = Flask(__name__)


UPLOAD_FOLDER = 'C:\\Users\\amith\\Documents\\GitHub\\udemy\\9 - Automatic Number Plate Recognition using ResNet and CNN\\app\\static'
ALLOWED_EXTENSIONS = set(['jpeg'])
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
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.jpeg')
        file1.save(path)
        data,w,h = image_pre(path)
        xmin,xmax,ymin,ymax = predict(data,w,h)
        img_arr = cv2.imread(path)
        img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
        plt.switch_backend('Agg') 
        fig,ax = plt.subplots()
        ax.imshow(img_arr)
        rect = patches.Rectangle((xmin,ymin), xmax-xmin,ymax-ymin, linewidth=2, edgecolor='c', facecolor='none')
        ax.add_patch(rect)
        plt.savefig(f'{UPLOAD_FOLDER}\\output.jpeg')
    return render_template('index.html') 





if __name__ == "__main__":
    app.run(debug=True)