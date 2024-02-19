from flask import *
from model.model import *
import numpy as np

app = Flask(__name__)
important_features = ["MEAN_RR", "RMSSD", "pNN25", "pNN50", "LF", "HF", "LF_HF"]
st=""

@app.route("/", methods = ["GET","POST"])
def hello():
    entries = []
    if request.method == "POST":
        for i in important_features:
            try:
                entries.append(float(request.form[i]))
            except ValueError:
                entries.append(request.form[i])
        p = predict(np.array(entries).reshape(-1,1))
        p = np.argmax(p[0])

        if p == 0:
            st = "No Stress"
        elif p == 1:
            st = "Low Stress"
        else:
            st = "High"
    else:
        st=""
    return render_template('index.html', cond=st)




if __name__ == "__main__":
    app.run(debug=True)