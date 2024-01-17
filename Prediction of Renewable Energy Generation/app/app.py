import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from model import *
from flask import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET','POST'])
def predict():
    initial_date = request.form['fd']
    final_date = request.form['td']
    df = retrieve_data_frame_for_plotting_graph(initial_date,final_date)
    features = df.columns.values
    future_values = model.predict(df[features])
    future_df = pd.DataFrame(data={'Predictions':future_values}, index = df.index)
    plt.switch_backend('Agg')
    plt.figure(figsize=(20,5))
    plt.plot(future_df['Predictions'])
    file_to_save = base + "/static/output.png"
    plt.savefig(file_to_save)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

