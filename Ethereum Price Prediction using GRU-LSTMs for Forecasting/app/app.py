from flask import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from model import generate_dates, generate_future_targets

app = Flask(__name__)

df = pd.read_csv("ETH_1H.csv",parse_dates=["Date"],index_col=["Date"])
df = df.sort_index()

@app.route("/")
def home():
    return render_template("templates/index.html")

@app.route("/", methods=["GET","POST"])
def predict():
    future_end_date = request.form["td"]
    future_dates = generate_dates(future_end_date)
    new_targets = generate_future_targets(future_dates)
    plt.switch_backend("Agg")
    plt.figure(figsize=(20,6))
    plt.figure(facecolor="black",dpi=300)
    ax = plt.axes()
    ax.set_facecolor("black")
    plt.plot(new_targets,linewidth=0.5,color="red",label="Future")
    plt.plot(df["Close"],linewidth=0.5,color="white",label="Past")
    plt.legend()

    plt.savefig("static/output.png")

    return render_template("templates/index.html")





if __name__ == "__main__":
    app.run(debug=True)


#%%
