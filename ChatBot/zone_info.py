import json
import requests
import pandas as pd 

def get_data():

    r = requests.get("https://api.covid19india.org/zones.json")
    data = r.json()
    return(data["zones"])

data = get_data()


def state():

    global data

    stt_lst = []
    for x in data:
        if x["state"] == "State Unassigned":
            continue
        if x["state"] not in stt_lst:
            stt_lst.append(x["state"] )

    print(stt_lst)


def zone_info_fun(state):

    global data 

    #state_lst = []
    dist_lst = []
    zone_lst = []
    lastupdate = []

    for district in data:
        #state_lst.append(district["state"])
        if state==district["state"]:
            dist_lst.append(district["district"])
            zone_lst.append(district["zone"])
            lastupdate.append(district["lastupdated"])

    dist_df = pd.DataFrame(dist_lst)
    zone_df = pd.DataFrame(zone_lst)
    lastupdate_df = pd.DataFrame(lastupdate)
    
    zone_info = pd.concat([dist_df,zone_df,lastupdate_df],axis=1).to_numpy()
    
    print(zone_info)
    return zone_info



def zone_info_fun_dis(district):

    global data 
    
    for x in data:
        if x["district"]==district:
            return x
    
    return 0




if __name__=="__main__":
    #print(zone_info_fun("Karnataka"))
    zone_info_fun_dis()

