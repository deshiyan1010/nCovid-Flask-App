import json
import requests
import pandas as pd 


def get_data():

    r = requests.get("https://api.covid19india.org/state_district_wise.json")
    data = r.json()
    return data

data = get_data()

# def state():

#     global data
#     stt_lst = []
#     for x,y in data.items():
#         if x == "State Unassigned":
#             continue
#         if x not in stt_lst:
#             stt_lst.append(x)

#     print(stt_lst)

def districtwise_info(state):
    
    global data
    state_dict = data[state]["districtData"]
    dist_lst = []
    conf_lst = []
    rec_lst = []
    des_lst = []
    act_lst = []

    for district,_ in state_dict.items():
        
        if district=="Unknown":
            continue
        district_dict = state_dict[district]
        dist_lst.append(district)
        conf_lst.append(district_dict["confirmed"])
        act_lst.append(district_dict["active"])
        des_lst.append(district_dict["deceased"])
        rec_lst.append(district_dict["recovered"])

    conf_df = pd.DataFrame(conf_lst)
    rec_df = pd.DataFrame(rec_lst)
    des_df = pd.DataFrame(des_lst)
    act_df = pd.DataFrame(act_lst)
    dist_df = pd.DataFrame(dist_lst)
    
    district_info = pd.concat([dist_df,conf_df,act_df,rec_df,des_df],axis=1).to_numpy()
    return district_info


if __name__=="__main__":
    
    #combined = districtwise_info("Karnataka")

    #combined.to_csv("check.csv")
    state()