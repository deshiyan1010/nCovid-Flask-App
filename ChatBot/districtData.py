import json
import requests
import pandas as pd 
import os
import numpy as np
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


def distDataList():

    global data
    distlst = []
    state_dict = {}
    intermediate_lst = []
    district_only = []
    state_only = []
    data_lst = list(data.values())

    for i,_ in data.items():
        state_only.append(i)


    for data in data_lst:

        for y in list(data.values()):

            if len(y)==2:
                continue
            else:
                intermediate_lst.append(y)


    for x in intermediate_lst:
        district_only.append(list(x))

    for  i in range(len(state_only)):
        state_only[i] = state_only[i].replace(" ","")

    print(state_only)

    # dicti = {}

    # for key,value in zip(state_only,district_only):

    #     dicti[key]=value

    # value_lst = []       
    # for key, values in dicti.items():
    #     value_lst+=values
    
        # f = open(os.path.join("aks",str(key)+".txt"),"w+")
        # for value in values:
        #     f.write("<option>")
        #     f.write(value)
        #     f.write("</option>")
        #     f.write("\n")


    # for state in state_only:    
    #     if state!="StateUnassigned":
    #         f = open(os.path.join("aks",str(state)+".txt"),"w+")
    #         for dis in district_only:
    #             for x in dis:
    #                 if x!="Unassigned":
    #                     f.write("<option>")
    #                     f.write(x)
    #                     f.write("</option>")
    #                     f.write("\n")
        
                





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


def districtwise_info_dist(dist):
    
    global data
    lst = list(data.values())
    dic = {}
    for x in lst:
        dat = x["districtData"]
        try:    
            b = list(dat[dist].values())
            act = b[1]
            conf = b[2]
            dec = b[3]
            rec = b[4]
            dic[dist] = [act,conf,dec,rec]
        except Exception as e:
            pass

    
    return dic


    # state_dict = data[state]["districtData"]
    # dist_lst = []
    # conf_lst = []
    # rec_lst = []
    # des_lst = []
    # act_lst = []

    # for district,_ in state_dict.items():
        
    #     if district=="Unknown":
    #         continue
    #     district_dict = state_dict[district]
    #     dist_lst.append(district)
    #     conf_lst.append(district_dict["confirmed"])
    #     act_lst.append(district_dict["active"])
    #     des_lst.append(district_dict["deceased"])
    #     rec_lst.append(district_dict["recovered"])

    # conf_df = pd.DataFrame(conf_lst)
    # rec_df = pd.DataFrame(rec_lst)
    # des_df = pd.DataFrame(des_lst)
    # act_df = pd.DataFrame(act_lst)
    # dist_df = pd.DataFrame(dist_lst)
    
    # district_info = pd.concat([dist_df,conf_df,act_df,rec_df,des_df],axis=1).to_numpy()
    # return district_info



if __name__=="__main__":
    
    #combined = districtwise_info("Karnataka")

    #combined.to_csv("check.csv")
    #state()
    print(districtwise_info_dist("Uttar Dinajpur"))