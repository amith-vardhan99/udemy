from flask import Flask, render_template, request
import numpy as np
import os
from model import image_preprocess,image_predict


app = Flask(__name__)


UPLOAD_FOLDER = 'C:\\Users\\amith\\Documents\\GitHub\\udemy\\6 - Age and Gender Prediction from Chest X-Ray Scans using CNN and OpenCV\\app\\static'
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
        data = image_preprocess(path)
        age,gen = image_predict(data)
        if gen == 1:
            result = 'Predicted age is '+str(np.int64(np.round(age,0)))+' years and the person is a Male'
        else:
            result = 'Predicted age is '+str(np.int64(np.round(age,0)))+' years and the person is a Female'
    return render_template('index.html',result=result)





if __name__ == "__main__":
    app.run(debug=True)