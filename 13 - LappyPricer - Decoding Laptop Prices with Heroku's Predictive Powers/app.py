import streamlit as st
import numpy as np
import pickle
import pandas as pd

st.title("Laptop Price Predictor")

#-------------------------------------------------------------------------------------------------------------------------
company_list = ['Acer', 'Apple', 'Asus', 'Chuwi', 'Dell', 'Fujitsu','Google', 'HP', 'Huawei', 'LG', 'Lenovo', 'MSI', 'Mediacom', 'Microsoft', 'Razer', 'Samsung', 'Toshiba', 'Vero', 'Xiaomi']
company = st.selectbox(label="Select the company of your laptop",options=tuple(company_list))
company_dict = {}
for i in company_list[1:]:
    if i == company:
        company_dict["Company_"+i] = 1
    else:
        company_dict["Company_"+i] = 0
#-------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------------------
typename_list = ['2 in 1 Convertible', 'Gaming', 'Netbook', 'Notebook', 'Ultrabook', 'Workstation']
typename = st.selectbox(label="Select the type of your laptop",options=tuple(typename_list))
typename_dict = {}
for i in typename_list[1:]:
    if i == company:
        typename_dict["TypeName_"+i] = 1
    else:
        typename_dict["TypeName_"+i] = 0
#-------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------
cpu_list = ['AMD A10-Series', 'AMD A12-Series', 'AMD A4-Series', 'AMD A6-Series', 'AMD A8-Series', 'AMD A9-Series', 'AMD E-Series', 'AMD Fx', 'AMD Ryzen 1600', 'AMD Ryzen 1700', 'Intel Atom', 'Intel Celeron Dual Core', 'Intel Celeron Quad Core', 'Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Intel Core m', 'Intel Pentium Dual Core', 'Intel Pentium Quad Core', 'Intel Xeon', 'Samsung Cortex']
cpu = st.selectbox("Select the CPU your laptop uses",options=tuple(cpu_list))
cpu_dict = {}
for i in cpu_list[1:]:
    if i == cpu:
        cpu_dict["Cpu_"+i] = 1
    else:
        cpu_dict["Cpu_"+i] = 0
#---------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------
ram = st.text_input(label="Enter the size of your laptop's RAM")
ram = ram.strip()
if ram == "":
    ram = 0
else:
    ram = int(ram)
#---------------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------
gpu_list = ['AMD', 'ARM', 'Intel', 'Nvidia']
gpu = st.selectbox(label="Select the GPU your laptop uses",options=tuple(gpu_list))
gpu_dict = {}
for i in gpu_list[1:]:
    if i == gpu:
        gpu_dict["Gpu_"+i] = 1
    else:
        gpu_dict["Gpu_"+i] = 0
#---------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------
opsys_list = ['Android', 'Chrome OS', 'Linux', 'Mac', 'No OS', 'Windows']
opsys = st.selectbox(label="Enter the operating system your laptop uses",options=tuple(opsys_list))
opsys_dict = {}
for i in opsys_list[1:]:
    if i == opsys:
        opsys_dict["OpSys_"+i] = 1
    else:
        opsys_dict["OpSys_"+i] = 0
#---------------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------
weight = st.text_input("Enter your laptop's weight")
if weight == "":
    weight = 0
else:
    weight = float(ram)
#---------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------
touchscreen_str = st.radio(label="Is your laptop a touchscreen one?", options=["Yes", "No"])
if touchscreen_str == "Yes":
    touchscreen = 1
else:
    touchscreen = 0
#---------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------
ips_str = st.radio(label="Does your screen use In-Plane Switching (IPS) technology?", options=["Yes", "No"])
if ips_str == "Yes":
    ips = 1
else:
    ips = 0
#---------------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------
hdd = st.selectbox(label="Select the size of Hard Disk Drive",options=("0", "1", "8", "16", "32", "128", "180", "240", "256", "500", "512", "1024", "2048"))
hdd = int(hdd)
#---------------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------
ssd = st.selectbox(label="Select the size of Solid State Drive",options=("0", "1", "8", "16", "32", "128", "180", "240", "256", "500", "512", "1024", "2048"))
ssd = int(ssd)
#---------------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------
screenlength = st.text_input(label="Enter the length of the screen")
if screenlength == "":
    screenlength = 0
else:
    screenlength = float(screenlength)
#---------------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------
screenwidth = st.text_input(label="Enter the width of the screen")
if screenwidth == "":
    screenwidth = 0
else:
    screenwidth = float(screenwidth)
#---------------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------
inches = st.text_input(label="Enter the number of inches for the screen")
if inches == "":
    inches = 0
else:
    inches = float(inches)
#---------------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------
ppi = np.sqrt(screenlength * screenlength + screenwidth * screenwidth)/inches
#---------------------------------------------------------------------------------------------------------------------------------



cols = ['Company_Apple', 'Company_Asus', 'Company_Chuwi', 'Company_Dell','Company_Fujitsu', 'Company_Google', 'Company_HP', 'Company_Huawei','Company_LG', 'Company_Lenovo', 'Company_MSI', 'Company_Mediacom','Company_Microsoft', 'Company_Razer', 'Company_Samsung','Company_Toshiba', 'Company_Vero', 'Company_Xiaomi', 'TypeName_Gaming','TypeName_Netbook', 'TypeName_Notebook', 'TypeName_Ultrabook','TypeName_Workstation', 'Cpu_AMD A12-Series', 'Cpu_AMD A4-Series','Cpu_AMD A6-Series', 'Cpu_AMD A8-Series', 'Cpu_AMD A9-Series','Cpu_AMD E-Series', 'Cpu_AMD Fx', 'Cpu_AMD Ryzen 1600','Cpu_AMD Ryzen 1700', 'Cpu_Intel Atom', 'Cpu_Intel Celeron Dual Core','Cpu_Intel Celeron Quad Core', 'Cpu_Intel Core i3', 'Cpu_Intel Core i5','Cpu_Intel Core i7', 'Cpu_Intel Core m', 'Cpu_Intel Pentium Dual Core','Cpu_Intel Pentium Quad Core', 'Cpu_Intel Xeon', 'Cpu_Samsung Cortex','Gpu_ARM', 'Gpu_Intel', 'Gpu_Nvidia', 'OpSys_Chrome OS', 'OpSys_Linux','OpSys_Mac', 'OpSys_No OS', 'OpSys_Windows', 'Ram', 'Weight','TouchScreen', 'IPS', 'PPI', 'ssd', 'hdd']

df = pd.DataFrame(columns=cols)

for i in company_dict:
    df.loc[0,i] = company_dict[i]
for i in typename_dict:
    df.loc[0,i] = typename_dict[i]
for i in cpu_dict:
    df.loc[0,i] = cpu_dict[i]
for i in gpu_dict:
    df.loc[0,i] = gpu_dict[i]
for i in opsys_dict:
    df.loc[0,i] = opsys_dict[i]
df.loc[0,"Ram"] = ram
df.loc[0,"Weight"] = weight
df.loc[0,"TouchScreen"] = touchscreen
df.loc[0,"IPS"] = ips
df.loc[0,"PPI"] = ppi
df.loc[0,"ssd"] = ssd
df.loc[0,"hdd"] = hdd



with open(file="model.pkl",mode="rb") as fi:
    model = pickle.load(fi)

if st.button(label="Predict Price"):
    predicted_price = model.predict(df)
    st.write("Predicted Price   :  "+str(np.round(predicted_price,2)[0]))