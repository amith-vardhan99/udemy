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
from wordcloud import *
import emoji

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

def return_wordcloud(user_messages,user):
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

    text = ""
    for i in words:
        text += (i + " ")
    
    wc = WordCloud(width=400,height=400,margin=4,random_state=np.random.randint(0,1000))
    word_cloud = wc.generate(text)
    ax = plt.figure()
    plt.imshow(word_cloud)

    return ax

def return_most_common_words(user_messages,user):
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

    words_series = pd.Series(words)
    words_count = pd.DataFrame(words_series.value_counts()).reset_index()
    words_count = words_count.sort_values(by="count",ascending=False)
    words_count_10 = words_count.head(10)


    ax1 = plt.figure()
    plt.barh(y=words_count_10["index"],width=words_count_10["count"])
    plt.xlabel("Number of words ------>")
    plt.ylabel("Words ------>")

    return ax1

def retrieve_emoji_count(user_messages,user):
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

    text = ""
    for i in words:
        text += (i + " ")

    list_of_emojis = []
    for i in emoji.EMOJI_DATA:
        list_of_emojis.append(i)
    list_of_emojis = np.array(list_of_emojis)

    emojis = []

    for i in text:
        if i in list_of_emojis:
            emojis.append(i)

    emojis = pd.DataFrame(emojis)
    emojis_count = pd.DataFrame(emojis.value_counts()).reset_index()
    emojis_count.columns = ["Emoji","Count"]

    emojis_count_percentage = emojis_count.copy()
    emojis_count_percentage["Percentage Use"] = emojis_count_percentage["Count"] * 100 / emojis_count_percentage["Count"].sum()
    return emojis_count,emojis_count_percentage

def retrieve_monthly_timeline(df_no_groups,user):
    dates_and_users = df_no_groups[["Only Date","User"]].reset_index(drop=True)
    if user=="Overall":
        dates = df_no_groups["Only Date"].values
    else:
        dates = df_no_groups[df_no_groups["User"]==user]["Only Date"].values
    
    date_count = pd.DataFrame(columns=["Date"])
    date_count["Date"] = dates

    date_count["Date"] = pd.to_datetime(date_count["Date"])
    date_count = date_count.sort_values(by=["Date"])
    date_count["Month"] = date_count["Date"].dt.month
    date_count["Year"] = date_count["Date"].dt.year
    date_count = date_count[["Month","Year"]]
    #date_count.columns = ["Date","Count"]

    #ax_5 = plt.figure()
    #plt.plot(["index"],ax_5["count"])
    date_count = pd.DataFrame(date_count.value_counts()).reset_index()

    date_count = date_count.sort_values(by=["Month","Year"]).reset_index(drop=True)
    date_count = date_count.astype("int64")

    date_count["Month"] = date_count["Month"].map({
        1:"January",
        2:"February",
        3:"March",
        4:"April",
        5:"May",
        6:"June",
        7:"July",
        8:"August",
        9:"September",
        10:"October",
        11:"November",
        12:"December"
    })

    date_count["Date"] = list(map(lambda x,y: x+"-"+str(y),date_count["Month"],date_count["Year"]))
    date_count = date_count[["Date","count"]]

    ax_5 = plt.figure()
    plt.plot(date_count["Date"],date_count["count"])
    plt.xlabel("Time ------>")
    plt.ylabel("Number of words ------>")

    return ax_5