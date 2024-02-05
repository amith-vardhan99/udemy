from flask import Flask, render_template, request
import sys
sys.path.append('C:/Users/amith/Documents/GitHub/udemy/Predicting Diamond Sales Price with Multiple Regression Methods/templates')
from model import model
import os

app = Flask(__name__)

path = os.getcwd().replace("\\","/")
list_of = ""
with open("model/list_of_features.txt","r+") as fl:
    list_of = fl.read()
list_of = list_of.split("\n")
list_of_features = list_of[0].split(", ")
list_of_dtypes = list_of[1].split(", ")



@app.route("/", methods = ["GET","POST"])
def hello():
    l=[]
    if request.method == "POST":
        for i in list_of_features:
            try:
                l.append(float(request.form[i]))
            except ValueError:
                l.append(request.form[i])
        sales_p = model.predict_total_sale_price(l)
        #print(sales_p)



    return render_template('index.html', sale=sales_p)







@app.route("/sub", methods = ['POST'])
def submit():
    if request.method == "POST":
        cut = request.form['cut']
    return render_template('sub.html', v1 = cut)


if __name__ == "__main__":
    app.run(debug=True)
#%%
