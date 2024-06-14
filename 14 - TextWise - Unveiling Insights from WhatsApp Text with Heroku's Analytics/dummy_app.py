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

df = preprocess("WhatsApp Chat with CodeAcuity.txt")
df_no_groups = df[df["User"]!="Group Notification"]
list_of_users = np.sort(df_no_groups["User"].unique())

user_messages = {}

user_messages["Overall"] = df_no_groups["Message"].values

for i in list_of_users:
    user_messages[i] = df_no_groups[df_no_groups["User"]==i]["Message"].values

side_title = st.sidebar.title("WhatsApp Chat Analyser")
file_name = st.sidebar.file_uploader(label="Choose a file from the computer")
print(file_name)