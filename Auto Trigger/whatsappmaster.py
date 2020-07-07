
#from whatsappMessager import message
from messNew import message
from whatsappDataExt import data
from db_push_get import commit,pull,save_csv
from datetime import date
from time import sleep
import warnings
warnings.filterwarnings("ignore")

def send():

    csv = pull("db.csv")

    for record in csv.iterrows():

        record = record[1]

        try:

            if int(record["DaysLeft"])>=0:




                print(record["Name"])

                india_data_cum,state_data_cum,district_data_cum,india_data_daily,state_data_daily,district_data_daily = data(record["State"],record["District"])

                
                #Cum
                india_conf = int(india_data_cum["Confirmed"])
                india_recovered = int(india_data_cum["Recovered"])
                india_des = int(india_data_cum["Deceased"])

                state_conf = int(state_data_cum["Confirmed"])
                state_recovered = int(state_data_cum["Recovered"])
                state_des = int(state_data_cum["Deceased"])

                dist_conf = int(district_data_cum["Confirmed"])
                dist_act = int(district_data_cum["Active"])
                dist_recovered = int(district_data_cum["Recovered"])
                dist_dec = int(district_data_cum["Deceased"])



                #Daily
                india_conf_d = int(india_data_daily["Confirmed"])
                india_recovered_d = int(india_data_daily["Recovered"])
                india_des_d = int(india_data_daily["Deceased"])

                state_conf_d = int(state_data_daily["Confirmed"])
                state_recovered_d = int(state_data_daily["Recovered"])
                state_des_d = int(state_data_daily["Deceased"])

                dist_conf_d = int(district_data_daily["Confirmed"])
                dist_act_d = int(district_data_daily["Active"])
                dist_recovered_d = int(district_data_daily["Recovered"])
                dist_dec_d = int(district_data_daily["Deceased"])

#                 rec_str ="h"
#                 rec_str = "The record according to sources as on {}-\n \
#     Cummilative\n \
#     India\n \
#     Confirmed {} \n \
#     Recovered {} \n \
#     Deceased {} \n\n \
#     State-{} \n \
#     Confirmed {} \n \
#     Recovered {} \n \
#     Deceased {} \n\n \
#     District-{} \n \
#     Confirmed {} \n \
#     Active {}\n \
#     Recovered {} \n \
#     Deceased {} \n\n\
#     Yesturdays' report\n \
#     India\n \
#     Confirmed {} \n \
#     Recovered {} \n \
#     Deceased {} \n\n \
#     State-{} \n \
#     Confirmed {} \n \
#     Recovered {} \n \
#     Deceased {} \n\n \
#     District-{} \n \
#     Confirmed {} \n \
#     Active {}\n \
#     Recovered {} \n \
#     Deceased {} \n\n\
# To visit the Covid website for more information \
# \nhttps://bit.ly/3djKf0C. If the link is not clickable please do reply. \n\
#     ".format(date.today(),india_conf, india_recovered, india_des, record["State"],state_conf,
#                             state_recovered,state_des,record["District"],dist_conf,
#                             dist_act,dist_recovered,dist_dec,
#                             india_conf_d, india_recovered_d, india_des_d, record["State"],state_conf_d,
#                             state_recovered_d,state_des_d,record["District"],dist_conf_d,
#                             dist_act_d,dist_recovered_d,dist_dec_d)







                rec_str = "The record according to sources as on {}-\n \
    Cummilative\n \
    India\n \
    Confirmed {} \n \
    Recovered {} \n \
    Deceased {} \n\n \
    State-{} \n \
    Confirmed {} \n \
    Recovered {} \n \
    Deceased {} \n\n \
    District-{} \n \
    Confirmed {} \n \
    Active {}\n \
    Recovered {} \n \
    Deceased {} \n\n\
    Yesturdays' report\n \
    India\n \
    Confirmed {} \n \
    Recovered {} \n \
    Deceased {} \n\n \
    State-{} \n \
    Confirmed {} \n \
    Recovered {} \n \
    Deceased {} \n\n \
To visit the Covid website for more information \
\nhttps://bit.ly/3djKf0C. If the link is not clickable please do reply. \n\
    ".format(date.today(),india_conf, india_recovered, india_des, record["State"],state_conf,
                            state_recovered,state_des,record["District"],dist_conf,
                            dist_act,dist_recovered,dist_dec,
                            india_conf_d, india_recovered_d, india_des_d, record["State"],state_conf_d,
                            state_recovered_d,state_des_d)








                if int(record["DaysLeft"])==0:
                    message(record["Country Code"],record["Phone Number"],"Your plan is over. Please recharge to avail service.")

                else:
                    message(record["Country Code"],record["Phone Number"],rec_str)
                

        except Exception as e:
            print("Not sent:" ,record["Name"])


    csv["DaysLeft"]=csv["DaysLeft"]-1
    csv.to_csv("db.csv")
    commit("db.csv")

def add_user(name,country_code,phone_number,state,district):

    csv = pull()
    if phone_number not in (csv["Phone Number"]):
        csv.loc[-1] = [str(name),str(country_code),str(phone_number),3,str(state),str(district)]
        csv.to_csv("db.csv")
        commit()
        return 1

    else:
        return 0

if __name__=="__main__":
    #add_user("Bibhu",91,8095646028,"Karnataka","Bengaluru Urban")
    send()