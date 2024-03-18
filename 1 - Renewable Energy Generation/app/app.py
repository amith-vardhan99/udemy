import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from model import *
from flask import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["GET","POST"])
def predict():
    initial_date = request.form["fd"]
    final_date = request.form["td"]
    df,future_dates = retrieve_data_frame_for_plotting_graph(initial_date,final_date)
    features = df.columns.values
    future_values = model.predict(df[features])
    future_df = pd.DataFrame(data={"Prediction" : future_values}, index = future_dates)
    plt.switch_backend("Agg")
    fig,ax = plt.subplots(figsize=(20,5))
    sns.lineplot(ax=ax,x=future_dates,y=future_df["Prediction"])
    ax.set(title="Predicted Renewable Energy")
    file_to_save = base + "/static/output.png"
    plt.savefig(file_to_save)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

