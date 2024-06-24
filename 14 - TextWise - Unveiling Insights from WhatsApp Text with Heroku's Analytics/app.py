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
from stats import *



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

    cols = st.columns(4)

    counting_parameters = retrieve_all_counting_parameters(user_messages,user)

    with cols[0]:
        st.header("Total Messages")
        st.title(counting_parameters[0])
    with cols[1]:
        st.header("Total No. of Words")
        st.title(counting_parameters[1])
    with cols[2]:
        st.header("Media Shared")
        st.title(counting_parameters[2])
    with cols[3]:
        st.header("Total Links Shared")
        st.title(counting_parameters[3])
    
    st.header("Most Busy Users")

    cols = st.columns(2)

    ax,df_user_counts = return_busy_users(file_name=file_name,df=df)

    
    plt.savefig("amith.png")


    with cols[0]:
        st.pyplot(fig=ax)
    with cols[1]:
        st.write(df_user_counts)

    st.header("Word Cloud")
    if user == "Sai Kiran Code Acuity":
        st.write("No Word Cloud for "+user)
    else:
        ax_2 = return_wordcloud(user_messages,user)
        st.pyplot(fig=ax_2)

    st.header("Most common words")

    ax_3 = return_most_common_words(user_messages,user)

    st.pyplot(fig=ax_3)

    st.header("Emoji Analysis")

    emoji_count,emoji_count_percentage = retrieve_emoji_count(user_messages,user)

    colus = st.columns(2)

    with colus[0]:
        st.write(emoji_count)
    with colus[1]:
        st.write(emoji_count_percentage)

    st.header("Monthly Timeline")

    ax_5 = retrieve_monthly_timeline(df_no_groups,user)

    st.pyplot(fig=ax_5)
    
