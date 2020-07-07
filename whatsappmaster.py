
from whatsappMessager import message
from whatsappDataExt import data
from db_push_get import commit,pull,save_csv
from datetime import date
from time import sleep
import warnings
warnings.filterwarnings("ignore")

def send():

    csv = pull()

    for record in csv.iterrows():

        record = record[1]

        try:

            if int(record["DaysLeft"])>=0:




                print(record["Name"])

                india_rec, state_rec, district_rec = data(record["State"],record["District"])

                india_conf = int(india_rec["Confirmed"])
                india_recovered = int(india_rec["Recovered"])
                india_des = int(india_rec["Deceased"])

                state_conf = int(state_rec["Confirmed"])
                state_recovered = int(state_rec["Recovered"])
                state_des = int(state_rec["Deceased"])

                dist_conf = int(district_rec["Confirmed"])
                dist_act = int(district_rec["Active"])
                dist_recovered = int(district_rec["Recovered"])
                dist_dec = int(district_rec["Deceased"])

                rec_str = "The record according to sources as on {}-\n \
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
    Deceased {} \n \
    To visit the Covid website for more information\
     https://bit.ly/3djKf0C .Please do reply with a '.' to keep a two way conversation. This is a must as to keep the connection established. If by any chance you dont get the updates then send 'join mountain-quarter' to this number again. \n\
    ".format(date.today(),india_conf, india_recovered, india_des, record["State"],state_conf,
                            state_recovered,state_des,record["District"],dist_conf,
                            dist_act,dist_recovered,dist_dec)

                if int(record["DaysLeft"])==0:
                    message(record["Country Code"],record["Phone Number"],"Your plan is over. Please recharge to avail service.")

                else:
                    message(record["Country Code"],record["Phone Number"],rec_str)
                sleep(5)

        except:
            print("Not sent:" ,record["Name"])


    csv["DaysLeft"]=csv["DaysLeft"]-1
    csv.to_csv("db.csv")
    commit()

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