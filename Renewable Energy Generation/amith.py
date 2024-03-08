import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import *
from sklearn.metrics import *
from sklearn.preprocessing import *
import warnings
warnings.filterwarnings("ignore")
from datetime import *
import joblib

df = pd.read_csv("Turbine_Data.csv")

df.head()

df_1 = df.set_index("Unnamed: 0")
df_1.head()

df_1.duplicated().sum()

df_2 = df_1.drop_duplicates()
df_2.head()

pp = df_2.nunique()
pp.head()

one_unique_value_cols = pp[pp==1].index.values
df_3 = df_2.drop(columns=one_unique_value_cols)
df_3.head()

df_3.describe()

df_4 = df_3[df_3["ActivePower"]>=0]
df_4.head()

(df_4.isna().sum() * 100 / df_4.isna().sum().sum()).round(2).head()

df_4.head()

df_5 = df_4.reset_index()
df_5.head()

df_6 = df_5.copy()
df_6["Unnamed: 0"] = pd.to_datetime(df_6["Unnamed: 0"])
df_6["date"] = df_6["Unnamed: 0"].dt.date
df_7 = df_6.drop(columns=["Unnamed: 0"])
df_8 = df_7.groupby(by="date").mean()
df_8.head()

mms = MinMaxScaler()

df_9 = pd.DataFrame(mms.fit_transform(df_8),columns=df_8.columns,index=df_8.index)
df_9.head()

features_required = df_9.columns.values.tolist()[1:]
target_required = df_9.columns.values.tolist()[0]
print("Features : ")
print(features_required)
print()
print("Target   : ")
print(target_required)

for i in features_required:
    fig,ax = plt.subplots(figsize=(15,5))
    sns.lineplot(ax=ax,x=df_9.index,y=df_9[i])
    sns.lineplot(ax=ax,x=df_9.index,y=df_9[target_required])
    ax.set(title=i+" vs "+target_required)

corr_matrix = df_9.corr()
fig,ax = plt.subplots(figsize=(15,15))
sns.heatmap(corr_matrix,annot=True,ax=ax,annot_kws={"weight":"bold"})

corr_matrix_sorted = corr_matrix["ActivePower"].sort_values(ascending=False)
final_columns = corr_matrix_sorted.iloc[0:2].index.values.tolist()
final_columns

df_final = df_4[final_columns]
df_final.dropna(inplace=True)

df_final.head()

train_length = round(len(df_final) * 0.75)
train_length

X_train = df_final.iloc[:train_length,1]
X_test = df_final.iloc[train_length:,1]
y_train = df_final.iloc[:train_length,0]
y_test = df_final.iloc[train_length:,0]
xgb_regr_1 = XGBRegressor(n_estimators=200)

xgb_regr_1.fit(X_train,y_train,eval_set=[(X_train,y_train),(X_test,y_test)],early_stopping_rounds=2,verbose=True)

y_pred = xgb_regr_1.predict(X_test)

y_pred[0:10]

target_df = pd.DataFrame(columns=["Actual","Predicted"],index=y_test.index)
target_df["Actual"] = y_test.copy()
target_df["Predicted"] = y_pred.copy()

target_df.head()

r2_score_xgboost = r2_score(target_df["Actual"],target_df["Predicted"])
mean_absolute_error_xgboost = mean_absolute_error(target_df["Actual"],target_df["Predicted"])
mean_squared_error_xgboost = mean_squared_error(target_df["Actual"],target_df["Predicted"])
mean_absolute_percentage_error_xgboost = mean_absolute_percentage_error(target_df["Actual"],target_df["Predicted"])

print("R2 score                        :  ",round(r2_score_xgboost,2))
print("Mean Absolute Error             :  ",round(mean_absolute_error_xgboost,2))
print("Mean Squared Error              :  ",round(mean_squared_error_xgboost,2))
print("Root Mean Squared Error         :  ",round(np.sqrt(mean_squared_error_xgboost),2))
print("Mean Absolute Percentage Error  :  ",round(mean_absolute_percentage_error_xgboost,2))

target_df_mod = target_df.reset_index()
target_df_mod["Unnamed: 0"] = pd.to_datetime(target_df_mod["Unnamed: 0"])
target_df_mod["date"] = target_df_mod["Unnamed: 0"].dt.date
target_df_daily = target_df_mod.groupby(by="date").mean()[["Actual","Predicted"]]
target_df_daily.head()

fig,ax = plt.subplots(figsize=(8,5))
sns.lineplot(x=target_df_daily.index,y=target_df_daily["Actual"])
sns.lineplot(x=target_df_daily.index,y=target_df_daily["Predicted"])
ax.set(title="Actual vs Predicted")

df_final_mod = df_final.reset_index()
df_final_mod["Unnamed: 0"] = pd.to_datetime(df_final_mod["Unnamed: 0"])
df_final_mod["date"] = df_final_mod["Unnamed: 0"].dt.date
df_final_daily = df_final_mod.groupby(by="date").mean()[["ActivePower","WindSpeed"]]

X_test_mod = X_test.reset_index()
X_test_mod["Unnamed: 0"] = pd.to_datetime(X_test_mod["Unnamed: 0"])
X_test_mod["date"] = X_test_mod["Unnamed: 0"].dt.date
X_test_mod_2 = X_test_mod.groupby(by="date").mean()["WindSpeed"]

target_df_daily_final = pd.DataFrame(columns=["ActivePower","WindSpeed"])
target_df_daily_final["ActivePower"] = target_df_daily["Predicted"].values
target_df_daily_final["WindSpeed"] = X_test_mod_2.values
target_df_daily_final.index = target_df_daily.index

target_df_daily_final.head()

fig,ax = plt.subplots(figsize=(15,5))
sns.lineplot(x=df_final_daily.index,y=df_final_daily["ActivePower"])
sns.lineplot(x=target_df_daily_final.index,y=target_df_daily_final["ActivePower"])
ax.set(title="Actual vs Predicted")

initial_date = datetime.fromisoformat("2020-04-01 12:00:00+00:00")
final_date = datetime.fromisoformat("2020-06-01 12:00:00+00:00")
interval = timedelta(minutes=10)
date_range = []
i = initial_date
future_dates = []

while i <= final_date:
    date_range.append(
        {"hour"           : i.hour,
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
df_future_dates.head()

dict_past_values = []
past_dates = []
for k in df_final.index.values:
    i = datetime.fromisoformat(k)
    dict_past_values.append(
        {"hour"           : i.hour,
         "minute"         : i.minute,
         "day"            : i.day,
         "month"          : i.month,
         "year"           : i.year,
         "dayofweek"      : 0 if i.weekday() == 6 else i.weekday() + 1,
         "dayofyear"      : i.timetuple().tm_yday,
         "calenderweek"   : i.isocalendar().week
         }
    )
    past_dates.append(i)
df_past_dates = pd.DataFrame(dict_past_values)
df_past_dates["ActivePower"] = df_final["ActivePower"].values

train_length_1 = round(len(df_past_dates) * 0.75)
train_length_1

X_train_1 = df_past_dates.loc[:train_length_1,:].drop(columns=["ActivePower"])
X_test_1 = df_past_dates.loc[train_length_1:,:].drop(columns=["ActivePower"]).reset_index(drop=True)
y_train_1 = df_past_dates.loc[:train_length_1,"ActivePower"]
y_test_1 = df_past_dates.loc[train_length_1:,"ActivePower"].reset_index(drop=True)

xgb_regr_2 = XGBRegressor(n_estimators=1000,learning_rate=0.01)

xgb_regr_2.fit(X_train_1,y_train_1,eval_set=[(X_train_1,y_train_1),(X_test_1,y_test_1)],early_stopping_rounds=2,verbose=True)

y_pred_1 = xgb_regr_2.predict(X_test_1)
y_pred_2 = xgb_regr_2.predict(df_future_dates)

target_df_1 = pd.DataFrame(columns=["Actual","Predicted"])
target_df_1["Actual"] = y_test_1.copy()
target_df_1["Predicted"] = y_pred_1.copy()

target_df_1.head()

r2_score_xgboost_1 = r2_score(target_df_1["Actual"], target_df_1["Predicted"])
mean_absolute_error_xgboost_1 = mean_absolute_error(target_df_1["Actual"], target_df_1["Predicted"])
mean_squared_error_xgboost_1 = mean_squared_error(target_df_1["Actual"], target_df_1["Predicted"])
mean_absolute_percentage_error_xgboost_1 = mean_absolute_percentage_error(target_df_1["Actual"], target_df_1["Predicted"])

print("R2 score                        :  ", round(r2_score_xgboost_1,2))
print("Mean Absolute Error             :  ", round(mean_absolute_error_xgboost_1,2))
print("Mean Squared Error              :  ", round(mean_squared_error_xgboost_1,2))
print("Root Mean Squared Error         :  ", round(np.sqrt(mean_squared_error_xgboost_1),2))
print("Mean Absolute Percentage Error  :  ", round(mean_absolute_percentage_error_xgboost_1,2))

print("With Wind Speed")
print()
print("R2 score                        :  ",round(r2_score_xgboost,2))
print("Mean Absolute Error             :  ",round(mean_absolute_error_xgboost,2))
print("Mean Squared Error              :  ",round(mean_squared_error_xgboost,2))
print("Root Mean Squared Error         :  ",round(np.sqrt(mean_squared_error_xgboost),2))
print("Mean Absolute Percentage Error  :  ",round(mean_absolute_percentage_error_xgboost,2))
print()
print()
print("Without Wind Speed")
print()
print("R2 score                        :  ", round(r2_score_xgboost_1,2))
print("Mean Absolute Error             :  ", round(mean_absolute_error_xgboost_1,2))
print("Mean Squared Error              :  ", round(mean_squared_error_xgboost_1,2))
print("Root Mean Squared Error         :  ", round(np.sqrt(mean_squared_error_xgboost_1),2))
print("Mean Absolute Percentage Error  :  ", round(mean_absolute_percentage_error_xgboost_1,2))

target_df_2 = df_future_dates.copy()
target_df_2["ActivePower"] = y_pred_2.copy()

target_df_2.head()
 md
df_1 -> Past values upto 75%
df_2 -> Past values last 25% - Actual and Predicted Values
df_3 -> Future Values
 md


X_train_1.head()

ddf_1 = X_train_1.copy()
ddf_1["Actual"] = y_train_1.copy()
ddf_1["Unnamed: 0"] = pd.to_datetime(past_dates[0:train_length+1])
ddf_1 = ddf_1[["Unnamed: 0","Actual"]]
ddf_1["date"] = ddf_1["Unnamed: 0"].dt.date
ddf_1.drop(columns=["Unnamed: 0"],inplace=True)
ddf_1 = ddf_1.groupby(by="date").mean()
ddf_1.head()

ddf_2 = X_test_1.copy()
ddf_2["Actual"] = y_test_1.copy()
ddf_2["Predicted"] = y_pred_1.copy()
ddf_2["Unnamed: 0"] = pd.to_datetime(past_dates[train_length:])
ddf_2 = ddf_2[["Unnamed: 0","Actual","Predicted"]]
ddf_2["date"] = ddf_2["Unnamed: 0"].dt.date
ddf_2.drop(columns=["Unnamed: 0"],inplace=True)
ddf_2 = ddf_2.groupby(by="date").mean()
ddf_2.head()

ddf_3 = target_df_2.copy()
ddf_3["Predicted"] = y_pred_2.copy()
ddf_3["Unnamed: 0"] = pd.to_datetime(future_dates)
ddf_3 = ddf_3[["Unnamed: 0","Predicted"]]
ddf_3["date"] = ddf_3["Unnamed: 0"].dt.date
ddf_3.drop(columns=["Unnamed: 0"],inplace=True)
ddf_3 = ddf_3.groupby(by="date").mean()
ddf_3.head()

ddf_4 = df_past_dates.copy()
ddf_4 = ddf_4.rename(columns={"ActivePower":"Actual"})
ddf_4["Unnamed: 0"] = pd.to_datetime(past_dates)
ddf_4 = ddf_4[["Unnamed: 0","Actual"]]
ddf_4["date"] = ddf_4["Unnamed: 0"].dt.date
ddf_4.drop(columns=["Unnamed: 0"],inplace=True)
ddf_4 = ddf_4.groupby(by="date").mean()
ddf_4.head()

fig,ax = plt.subplots(figsize=(8,5))
sns.lineplot(x=ddf_2.index,y=ddf_2["Actual"])
sns.lineplot(x=ddf_2.index,y=ddf_2["Predicted"])
ax.set(title="Actual vs Predicted")

fig,ax = plt.subplots(figsize=(15,5))
sns.lineplot(x=ddf_4.index,y=ddf_4["Actual"])
sns.lineplot(x=ddf_2.index,y=ddf_2["Predicted"])
ax.set(title="Actual vs Predicted")

fig,ax = plt.subplots(figsize=(15,5))
sns.lineplot(x=ddf_4.index,y=ddf_4["Actual"])
sns.lineplot(x=ddf_3.index,y=ddf_3["Predicted"])
ax.set(title="Past and Future Active Power")

fig,ax = plt.subplots(figsize=(15,5))
sns.lineplot(x=ddf_4.index,y=ddf_4["Actual"])
sns.lineplot(x=ddf_2.index,y=ddf_2["Predicted"])
sns.lineplot(x=ddf_3.index,y=ddf_3["Predicted"])
ax.set(title="Past Actual vs Predicted Active Powers, and Future Active Power")

xgb_regr_1.save_model("xgb_model_1.json")
xgb_regr_2.save_model("xgb_model_2.json")

#file_1 = open("xgb_model_1.joblib","wb")
file_2 = open("xgb_model_2.joblib","wb")
file_3 = open("app/xgb_model_2.joblib","wb")

joblib.dump(value=xgb_regr_2,filename=file_2)
joblib.dump(value=xgb_regr_2,filename=file_3)