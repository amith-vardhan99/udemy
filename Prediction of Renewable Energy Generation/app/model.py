import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
from xgboost import *
from datetime import *

base = os.getcwd()
file = base + "/xgb_model_2.pkl"
model = pickle.load(open(file, "rb"))

reg = XGBRegressor()

def retrieve_data_frame_for_plotting_graph(ini,fin):
    initial_date = datetime.fromisoformat(ini+" 12:00:00+00:00")
    final_date = datetime.fromisoformat(fin+" 12:00:00+00:00")
    interval = timedelta(minutes=10)
    date_range = []
    i = initial_date
    future_dates = []

    while i <= final_date:
        date_range.append(
            {
                "hour"           : i.hour,
                "minute"         : i.minute,
                "day"            : i.day,
                "month"          : i.month,
                "year"           : i.year,
                "dayofweek"      : 0 if i.weekday() == 6 else i.weekday() + 1,
                "dayofyear"      : i.timetuple().tm_yday,
                "calenderweek"   : i.isocalendar().week
             }
        )
        future_dates.append(i)
        i += interval

    df_future_dates = pd.DataFrame(date_range)

    return df_future_dates