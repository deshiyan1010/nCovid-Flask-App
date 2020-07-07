import pandas as pd
import io
import requests
import numpy as np 
import warnings

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



def get_table_cum():
  conf, rec, des = get_data()
  
  sum_conf = conf.sum(axis=0)
  sum_rec = rec.sum(axis=0)
  sum_des = des.sum(axis=0)

  sum_conf_refined = sum_conf.drop(index=["UN","Day num"])
  sum_rec_refined = sum_rec.drop(index=["UN","Day num"])
  sum_des_refined = sum_des.drop(index=["UN","Day num"])
  
  states = pd.DataFrame(sum_conf_refined.rename(index=code_state()).index.values)

  conf_final = pd.DataFrame(sum_conf_refined.reset_index(drop=True))
  rec_final = pd.DataFrame(sum_rec_refined.reset_index(drop=True))
  des_final = pd.DataFrame(sum_des_refined.reset_index(drop=True))
  
  return states,conf_final,rec_final,des_final


def get_table_daily():
  conf, rec, des = get_data()
  
  sum_conf_refined = conf.iloc[-1].drop(index=["UN","Day num"])
  sum_rec_refined = rec.iloc[-1].drop(index=["UN","Day num"])
  sum_des_refined = des.iloc[-1].drop(index=["UN","Day num"])

  states = pd.DataFrame(sum_conf_refined.rename(index=code_state()).index.values)


  conf_final = pd.DataFrame(sum_conf_refined.reset_index(drop=True))
  rec_final = pd.DataFrame(sum_rec_refined.reset_index(drop=True))
  des_final = pd.DataFrame(sum_des_refined.reset_index(drop=True))


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

    conf_csv.to_csv("conf.csv")
    rec_csv.to_csv("rec.csv")
    des_csv.to_csv("des.csv")

    return conf_csv, rec_csv, des_csv

def to_days(ts):

  num_days = (ts - pd.Timestamp("2020-03-14 00:00:00")).days
  return num_days

def to_date(num_lst):
  
  date_lst = []
  for x in num_lst:
    date_lst.append(pd.Timestamp("2020-03-14 00:00:00")+pd.to_timedelta(x,unit = "D"))
  return date_lst



if __name__=="__main__":
    #plot(cat="Confirmed",state="TN",till = "2020-07-01",cum_da = "Cumulative",stt_name="X")
    #print(get_table_cum())
    print(get_table_daily())