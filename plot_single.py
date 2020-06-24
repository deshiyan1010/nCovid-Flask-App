import pandas as pd
import io
import requests
from sklearn.linear_model import SGDClassifier
import numpy as np 
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import warnings
import plotly
import plotly.graph_objs as go
import os
from datetime import datetime
warnings.simplefilter("ignore")
# import plotly.express as px

def code_state():
    states = {'TT': 'Total India', 
    'AN': 'Andaman and Nicobar Islands', 
    'AP': 'Andra Pradesh', 
    'AR': 'Arunachal Pradesh', 
    'AS': 'Assam', 
    'BR': 'Bihar', 
    'CH': 'Chandigarh', 
    'CT': 'Chhattisgarh', 
    'DN': 'Dadra and Nagar Haveli', 
    'DD': 'Daman and Diu', 
    'DL': 'Delhi', 
    'GA': 'Goa', 
    'GJ': 'Gujarat', 
    'HR': 'Haryana', 
    'HP': 'Himachal Pradesh', 
    'JK': 'Jammu and Kashmir', 
    'JH': 'Jharkhand', 
    'KA': 'Karnataka', 
    'KL': 'Kerala', 
    'LA': 'Ladakh', 
    'LD': 'Lakshadweep', 
    'MP': 'Madhya Pradesh', 
    'MH': 'Maharashtra', 
    'MN': 'Manipur', 
    'ML': 'Meghalaya', 
    'MZ': 'Mizoram', 
    'NL': 'Nagaland', 
    'OR': 'Odisha', 
    'PY': 'Puducherry', 
    'PB': 'Punjab', 
    'RJ': 'Rajasthan', 
    'SK': 'Sikkim', 
    'TN': 'Tamil Nadu', 
    'TG': 'Telangana', 
    'TR': 'Tripura', 
    'UP': 'Uttar Pradesh', 
    'UT': 'Uttarakhand', 
    'WB': 'West Bengal'}
    return states



def get_table():
  conf, rec, des = get_data()
  
  sum_conf = conf.sum(axis=0)
  sum_rec = rec.sum(axis=0)
  sum_des = des.sum(axis=0)

  sum_conf_refined = sum_conf.drop(index=["UN","Day num"])
  sum_rec_refined = sum_rec.drop(index=["UN","Day num"])
  sum_des_refined = sum_des.drop(index=["UN","Day num"])
  
  # states = sum_conf_refined.rename(index=code_state()).index.values.tolist()
  # #rec_final = sum_rec_refined.rename(index=code_state())
  # #des_final = sum_des_refined.rename(index=code_state())

  # conf_final = sum_conf_refined.reset_index(drop=True).tolist()
  # rec_final = sum_rec_refined.reset_index(drop=True).tolist()
  # des_final = sum_des_refined.reset_index(drop=True).tolist()
  states = pd.DataFrame(sum_conf_refined.rename(index=code_state()).index.values)
  #rec_final = sum_rec_refined.rename(index=code_state())
  #des_final = sum_des_refined.rename(index=code_state())

  conf_final = pd.DataFrame(sum_conf_refined.reset_index(drop=True))
  rec_final = pd.DataFrame(sum_rec_refined.reset_index(drop=True))
  des_final = pd.DataFrame(sum_des_refined.reset_index(drop=True))

  # print(conf_final)
  # print("-"*100)
  # print(rec_final)
  # print("-"*100)
  # print(rec_final)
  # print("-"*100)
  # print(states)
  
  return states,conf_final,rec_final,des_final



def get_data():
    url = "https://api.covid19india.org/csv/latest/state_wise_daily.csv"
    s = requests.get(url).content
    csv = pd.read_csv(io.StringIO(s.decode("utf-8")))

    csv["Date"] = pd.to_datetime(csv["Date"])
    default_start_point = pd.Timestamp("2020-03-14 00:00:00")
    csv["Day num"] = csv["Date"] - default_start_point

    conf_csv = csv[csv["Status"] == "Confirmed"].drop(["Status"], axis=1)
    conf_csv["Day num"] = conf_csv["Day num"].dt.days

    rec_csv = csv[csv["Status"] == "Recovered"].drop(["Status"], axis=1)
    rec_csv["Day num"] = rec_csv["Day num"].dt.days

    des_csv = csv[csv["Status"] == "Deceased"].drop(["Status"], axis=1)
    des_csv["Day num"] = des_csv["Day num"].dt.days

    return conf_csv, rec_csv, des_csv

def to_days(ts):

  num_days = (ts - pd.Timestamp("2020-03-14 00:00:00")).days
  return num_days

def to_date(num_lst):
  
  date_lst = []
  for x in num_lst:
    date_lst.append(pd.Timestamp("2020-03-14 00:00:00")+pd.to_timedelta(x,unit = "D"))
  return date_lst


def plot(cat="Confirmed",state="TT",till = "2020-07-01",cum_da = "Cumulative",stt_name="X"):
  till=pd.Timestamp(str(till)+" 00:00:00")
  num_days = to_days(till)
  conf_csv, rec_csv, des_csv = get_data()


  if cat=="Recovered":
    X_train, y_train = np.array(rec_csv["Day num"]), np.array(rec_csv[state])

  if cat=="Deceased":
    X_train, y_train = np.array(des_csv["Day num"]), np.array(des_csv[state])

  if cat=="Confirmed":
    X_train, y_train = np.array(conf_csv["Day num"]), np.array(conf_csv[state])

  if cum_da=="Cumulative":
    y_train = y_train.cumsum()

  X = X_train.reshape(-1,1)
  vector = y_train.reshape(-1,1)


  poly = PolynomialFeatures(degree=7)
  X_ = poly.fit_transform(X)

  clf = linear_model.Lasso()
  clf.fit(X_, vector)


  num_days_lst = np.array(list(range(1,num_days+1)))
  a = poly.fit_transform(num_days_lst.reshape(-1,1))


  Predicted = go.Scatter(
      x=to_date(num_days_lst.ravel()),
      y=clf.predict(a).ravel(),name="Predicted"
  )
  Actual = go.Scatter(
      x=to_date(X.ravel()),
      y=vector.ravel(), name="Actual"
  )
  data = [Predicted,Actual]




  filex = str(cat)+str(state)+str(till.date())+str(datetime.now().microsecond)
  plotly.offline.plot({"data":data,"layout":go.Layout(title="Covid Predictor: "+str(cat)+" cases of "+str(stt_name))},filename="templates/"+str(filex)+".html",auto_open=False)

  return filex



if __name__=="__main__":
    #plot(cat="Confirmed",state="TN",till = "2020-07-01",cum_da = "Cumulative",stt_name="X")
    get_table()