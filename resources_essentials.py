import json
import requests
import pandas as pd 

def get_data():

    r = requests.get("https://api.covid19india.org/resources/resources.json")
    data = r.json()
    return(data["resources"])


data = get_data()


def district_lst_():

    global data
    dist_lst = {}
    
    state_lst = []

    for info in data:

        if info["state"] not in state_lst:
            state_lst.append(info["state"])
    
    
    
    for state in state_lst:
        lst=[]
        
        for info in data:
            if info["state"]==state:
                
                if info["city"] not in lst:
                    lst.append(info["city"])
        
        dist_lst["".join(state.split())]=",".join(lst)

    jx = json.dumps(dist_lst,indent=4)
    print(jx)
    # with open('json.json', 'w') as outfile:
    #     json.dump(dist_lst, outfile)

    return dist_lst
            

def dist_list():

    global data

    dist_lis = []

    for info in data:
        dist_lis.append(info["city"])

    dist_lis = set(dist_lis)
    dist_lis = list(dist_lis)
    dist_lis = sorted(dist_lis)


    return dist_lis




def resourse_info(district):

    global data

    category = []
    phone = []
    contact = []
    nameoforg = []
    desc = []
    for info in data:
        if district==info["city"]:
            category.append(info["category"])
            phone.append(info["phonenumber"])
            nameoforg.append(info["nameoftheorganisation"])
            desc.append(info["descriptionandorserviceprovided"])
    
    category_df = pd.DataFrame(category)
    phone_df = pd.DataFrame(phone)
    nameoforg_df = pd.DataFrame(nameoforg)
    desc_df = pd.DataFrame(desc)
    
    resource_info = pd.concat([category_df,phone_df,nameoforg_df,desc_df],axis=1).to_numpy()
    
    
    return resource_info

if __name__=="__main__":
    #resourse_info("Bangalore").to_csv("bangalore.csv")

    district_lst_()
