import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt    
import seaborn as sns    
import re   
import os   
import warnings
warnings.filterwarnings("ignore")
from preprocess import *
import streamlit as st


side_title = st.sidebar.title("WhatsApp Chat Analyser")
file = st.sidebar.file_uploader(label="Choose a file from the computer")

if file is not None:
    file_name = file.name

    df = preprocess(file_name=file_name)
    df_no_groups = df[df["User"]!="Group Notification"]
    list_of_users = np.sort(df_no_groups["User"].unique())

    user_messages = {}
    user_messages["Overall"] = df_no_groups["Message"].values
    for i in list_of_users:
        user_messages[i] = df_no_groups[df_no_groups["User"]==i]["Message"].values
    
    list_of_users = list(user_messages.keys())


    user = st.sidebar.selectbox(label="Select the person with respect to whom analysis should be made",options=list_of_users)

    