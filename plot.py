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
warnings.simplefilter("ignore")
# import plotly.express as px

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

  if cat=="Desceased":
    X_train, y_train = np.array(des_csv["Day num"]), np.array(des_csv[state])

  if cat=="Confirmed":
    X_train, y_train = np.array(conf_csv["Day num"]), np.array(conf_csv[state])

  if cum_da=="Cumulative":
    y_train = y_train.cumsum()

  X = X_train.reshape(-1,1)
  vector = y_train.reshape(-1,1)


  poly = PolynomialFeatures(degree=3)
  X_ = poly.fit_transform(X)

  clf = linear_model.Ridge()
  clf.fit(X_, vector)


  num_days_lst = np.array(list(range(1,num_days+1)))
  a = poly.fit_transform(num_days_lst.reshape(-1,1))
  # plt.plot(num_days_lst, (clf.predict(a)),"r")
  # plt.plot(X, vector,"b")
  # plt.show()

  Predicted = go.Scatter(
      x=to_date(num_days_lst.ravel()),
      y=clf.predict(a).ravel(),name="Predicted"
  )
  Actual = go.Scatter(
      x=to_date(X.ravel()),
      y=vector.ravel(), name="Actual"
  )
  data = [Predicted,Actual]
  plotly.offline.plot({"data":data,"layout":go.Layout(title="Covid Predictor: "+str(cat)+" cases of "+str(stt_name))},filename="templates/file.html",auto_open=False)
  #py.iplot([trace0,trace1])
  #trace0 = px.line(vector.ravel(),X.ravel())
  #trace1 = px.line(clf.predict(a).ravel(),num_days_lst.ravel())

  #return [trace0,trace1]


if __name__=="__main__":
    plot(cat="Confirmed",state="TN",till = "2020-07-01")