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

def retrieve_all_counting_parameters(user_messages,user):
    messages = user_messages[user]
    
    total_messages = len(messages)
    
    words_5 = ""
    for i in messages:
        words_5 += (i + " ")
    
    words_4 = re.sub(pattern="(https://\S+\s+)",repl="",string=words_5)
    words_3 = re.sub(pattern="(<Media omitted>)",repl="",string=words_4)
    words_2 = re.sub(pattern="(<This message was edited>)",repl="",string=words_3)
    words_11 = words_2.replace("\n", " ")
    words_1 = words_11.replace(".","")
    words = words_1.split(" ")

    while "" in words:
        words.remove("")

    total_no_of_words = len(words)

    media_shared = messages[messages=="<Media omitted>"].shape[0]

    list_of_links = re.findall(pattern="(https://\S+\s+)",string=words_5)
    links_shared = len(list_of_links)

    return total_messages,total_no_of_words,media_shared,links_shared

def return_busy_users(file_name,df):
    df_no_groups = df[df["User"]!="Group Notification"]
    df_user_counts = df["User"].value_counts()
    df_user_counts_chart = dict(df_user_counts.head())
    
    ax = plt.figure()
    plt.bar(x=df_user_counts_chart.keys(),height=df_user_counts_chart.values())
    plt.xticks(rotation=45)

    return ax,df_user_counts