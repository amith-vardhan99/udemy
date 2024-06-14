import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt    
import seaborn as sns    
import re   
import os   
import warnings
warnings.filterwarnings("ignore")


def retrieve_date_and_time(dat):
    p = dat.split(", ")
    p = list(map(lambda x: x.strip(),p))
    date = p[0]
    time_1 = p[1].split(" ")
    time_part = time_1[0]
    meridian = time_1[1]

    time_divisions = [int(i) for i in time_part.split(":")]

    if meridian == "AM" and time_divisions[0] == 12:
        time_divisions[0] = 0
    elif meridian == "PM" and time_divisions[0] >= 1 and time_divisions[0] < 12:
        time_divisions[0] += 12
    
    
    
    hour = str(time_divisions[0])
    minute = str(time_divisions[1])

    if len(minute) < 2:
        minute = ("0" + minute)

    final_time = date + " " + hour + ":" + minute
    
    return final_time

def preprocess(file_name):

    with open(file_name,"r",encoding="utf-8") as fi:
        text = fi.read()

    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[A-Z]M\s-\s"

    dates_1 = re.findall(pattern=pattern,string=text)
    dates_2 = list(map(lambda x: x.replace("\u202f", " "),dates_1))
    dates_3 = list(map(lambda x: x.split("-")[0].strip(),dates_2))
    dates = list(map(lambda x: retrieve_date_and_time(x),dates_3))

    text_1 = re.split(pattern=pattern,string=text)[1:]

    pat = "\w: "
    ent = list(map(lambda x: re.split("([\w\W]+?):\s",x),text_1))

    users = []
    messages = []

    for i in ent:
        ent_1 = i[1:]
        if len(ent_1) == 0:
            users.append("Group Notification")
            messages.append(i[0])
            continue
        ent_first = ent_1[0]
        ent_remaining = ent_1[1:]
        ent_remaining_combined = ""
        for j in ent_remaining:
            ent_remaining_combined += (j + "\n")
        while ent_remaining_combined[-1] == "\n":
            ent_remaining_combined = ent_remaining_combined[:-1]
        users.append(ent_first)
        messages.append(ent_remaining_combined)

    df = pd.DataFrame(columns=["Time","User","Message"])
    df_1 = df.copy()
    df["Time"] = dates
    df["Time"] = pd.to_datetime(df["Time"])
    df["User"] = users
    df["Message"] = messages

    final_df = pd.DataFrame(columns=["Message","Date","User","Only Date","Year","Month Number","Month","Day","Day Name","Hour","Minute"])

    final_df["Message"] = df["Message"]
    final_df["Date"] = df["Time"]
    final_df["User"] = df["User"]
    final_df["Only Date"] = df["Time"].dt.date
    final_df["Year"] = df["Time"].dt.year
    final_df["Month Number"] = df["Time"].dt.month
    final_df["Month"] = df["Time"].dt.month_name()
    final_df["Day"] = df["Time"].dt.day
    final_df["Day Name"] = df["Time"].dt.day_name()
    final_df["Hour"] = df["Time"].dt.hour
    final_df["Minute"] = df["Time"].dt.minute

    return final_df
