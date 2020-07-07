from flask import Flask, render_template, request
from plot_single import plot,get_table
import plotly
import os
import pandas as pd
import numpy as np
from districtData import districtwise_info
from resources_essentials import resourse_info, dist_list
from zone_info import zone_info_fun
from news_fun import news_mod
from nltk_do import install
from whatsappmaster import send, add_user
app = Flask(__name__,static_url_path='/static')

def mon_name_num(month):
    mon_dict = {"January":1,"February":2,"March":3,
              "April":4,"May":5,"June":6,"July":7,
              "August":8,"September":9,"October":10,
              "November":11,"December":12}
    return mon_dict[month]

def state_lst_orig():
    x = ["Total India","Andaman and Nicobar Islands","Andra Pradesh",
              "Arunachal Pradesh","Assam","Bihar",
              "Chandigarh",	"Chhattisgarh","Dadra and Nagar Haveli",
              "Daman and Diu","Delhi","Goa",
              "Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir",
              "Jharkhand","Karnataka",
              "Kerala",	"Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra",
              "Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry",
              "Punjab",
              "Rajasthan","Sikkim",	"Tamil Nadu","Telangana","Tripura",	"Uttar Pradesh",
              "Uttarakhand", "West Bengal"]
    return x

def state_code(state):
    states = {"Total India":"TT",	"Andaman and Nicobar Islands":"AN",	"Andra Pradesh":"AP", 
              "Arunachal Pradesh":"AR",	"Assam":"AS", "Bihar":"BR",
              "Chandigarh":"CH", "Chhattisgarh":"CT", "Dadra and Nagar Haveli":"DN",	
              "Daman and Diu":"DD",	"Delhi":"DL", "Goa":"GA",
              "Gujarat":"GJ", "Haryana":"HR", "Himachal Pradesh":"HP", 
              "Jammu and Kashmir":"JK",	"Jharkhand":"JH", "Karnataka":"KA",
              "Kerala":"KL", "Ladakh":"LA",	"Lakshadweep":"LD",	"Madhya Pradesh":"MP",	
              "Maharashtra":"MH", "Manipur":"MN",
              "Meghalaya":"ML",	"Mizoram":"MZ",	"Nagaland":"NL", "Odisha":"OR",	
              "Puducherry":"PY", "Punjab":"PB",
              "Rajasthan":"RJ",	"Sikkim":"SK", "Tamil Nadu":"TN", "Telangana":"TG",	
              "Tripura":"TR",	"Uttar Pradesh":"UP",
              "Uttarakhand":"UT", "West Bengal":"WB"}
    return states[state]

@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    states = state_lst_orig()
    months = ["January","February","March",
              "April","May","June","July",
              "August","September","October",
              "November","December"]
    dates = [str(x) for x in range(1,32)]
    years = ["2020","2021"]
    types = ["Confirmed","Recovered","Deceased"]
    cum_das = ["Cumulative","Daily"]

    state_lst,conf_final,rec_final,des_final = get_table()
    combined = pd.concat([state_lst,conf_final,rec_final,des_final],axis=1)
    combined.to_csv("check.csv")
    combined = combined.to_numpy()
  
    return render_template('index.html',states=states,
                           months=months,
                           dates=dates,
                           years=years,
                           types=types,
                           cum_das=cum_das,
                           combined=combined,
                           )

@app.route('/math', methods=['POST'])  # This will be called from UI
def math_operation():
    if (request.method=='POST'):
        sttNM = request.form['state']
        statex = state_code(sttNM)
        typex = request.form['type']
        datex = request.form['datex']
        cum_dax = request.form['cum_da']

        filex = plot(cat=str(typex),state=statex,till=str(datex),cum_da=str(cum_dax),stt_name=sttNM)

        return render_template(str(filex)+".html")


# Districtwise
@app.route('/statewise', methods=['GET', 'POST'])
def statewise():

    states = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 
    'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 
    'Delhi', 'Dadra and Nagar Haveli and Daman and Diu', 'Goa', 'Gujarat', 
    'Himachal Pradesh', 'Haryana', 'Jharkhand', 'Jammu and Kashmir', 
    'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Maharashtra', 
    'Meghalaya', 'Manipur', 'Madhya Pradesh', 'Mizoram', 'Nagaland', 
    'Odisha', 'Punjab', 'Puducherry', 'Rajasthan', 'Sikkim', 'Telangana', 
    'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']


    return render_template('statewisedata.html',
                            states=states)


@app.route('/statewisesub', methods=['GET', 'POST'])
def statewise_sub():

    states = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 
    'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 
    'Delhi', 'Dadra and Nagar Haveli and Daman and Diu', 'Goa', 'Gujarat', 
    'Himachal Pradesh', 'Haryana', 'Jharkhand', 'Jammu and Kashmir', 
    'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Maharashtra', 
    'Meghalaya', 'Manipur', 'Madhya Pradesh', 'Mizoram', 'Nagaland', 
    'Odisha', 'Punjab', 'Puducherry', 'Rajasthan', 'Sikkim', 'Telangana', 
    'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']

    state_dist = request.form['state']

    districtwise = districtwise_info(state_dist)


    return render_template('statewisedatasub.html',
                            states=states,
                            districtwise=districtwise)




# Resource
@app.route('/resourcemain', methods=['GET', 'POST'])
def resourse():

    return render_template('resources.html')

@app.route('/resourcesec', methods=['GET', 'POST'])
def resourseSec():

    districtList = dist_list()

    return render_template('resourcesSecondary.html',
                            districts = districtList)

@app.route('/resourcesub', methods=['GET', 'POST'])
def resourse_sub():


    res_dist = request.form['district']
    rec_dist_info = resourse_info(res_dist)


    return render_template('resourcesub.html',
                            rec_dist_info=rec_dist_info,
                          )



# Zones
@app.route('/zonemain', methods=['GET', 'POST'])
def zones():

    states = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 
    'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 
    'Delhi', 'Dadra and Nagar Haveli and Daman and Diu', 'Goa', 'Gujarat', 
    'Himachal Pradesh', 'Haryana', 'Jharkhand', 'Jammu and Kashmir', 
    'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Maharashtra', 
    'Meghalaya', 'Manipur', 'Madhya Pradesh', 'Mizoram', 'Nagaland', 
    'Odisha', 'Punjab', 'Puducherry', 'Rajasthan', 'Sikkim', 'Telangana', 
    'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']

    return render_template('zone.html',
                            states=states)


@app.route('/zonesub', methods=['GET', 'POST'])
def zones_sub():


    zone = request.form['state']

    zoneinfo = zone_info_fun(zone)


    return render_template('zonesub.html',
                            zoneinfo=zoneinfo,
                          )



@app.route('/news', methods=['GET', 'POST'])
def news():

    newsx = news_mod()
    return render_template('news.html',
                            newsx=newsx,
                          )



# ABout US
@app.route('/aboutus', methods=['GET', 'POST'])
def aboutus():

    return render_template('aboutus.html')

#How to use?
@app.route('/knowmore', methods=['GET', 'POST'])
def knowmorex():

    return render_template('knowmore.html')

#Whatsapp
@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():

    return render_template('wp.html')

#Whatsapp Red
@app.route('/whatsappsuc', methods=['GET', 'POST'])
def whatsapp_suc():

    name = request.form.get('name')
    code = int(request.form.get('country'))
    number = int(request.form.get('number'))

    state = request.form['state']
    district = request.form['district']

    state_dict = {'StateUnassigned': 'State Unassigned', 'AndamanandNicobarIslands': 'Andaman and Nicobar Islands', 'AndhraPradesh': 'Andhra Pradesh', 'ArunachalPradesh': 'Arunachal Pradesh', 'Assam': 'Assam', 'Bihar': 'Bihar', 'Chandigarh': 'Chandigarh', 'Chhattisgarh': 'Chhattisgarh', 'Delhi': 'Delhi', 'DadraandNagarHaveliandDamanandDiu': 'Dadra and Nagar Haveli and Daman and Diu', 'Goa': 'Goa', 'Gujarat': 'Gujarat', 'HimachalPradesh': 'Himachal Pradesh', 'Haryana': 'Haryana', 'Jharkhand': 'Jharkhand', 'JammuandKashmir': 'Jammu and Kashmir', 'Karnataka': 'Karnataka', 'Kerala': 'Kerala', 'Ladakh': 'Ladakh', 'Lakshadweep': 'Lakshadweep', 'Maharashtra': 'Maharashtra', 'Meghalaya': 'Meghalaya', 'Manipur': 'Manipur', 'MadhyaPradesh': 'Madhya Pradesh', 'Mizoram': 'Mizoram', 'Nagaland': 'Nagaland', 'Odisha': 'Odisha', 'Punjab': 'Punjab', 'Puducherry': 'Puducherry', 'Rajasthan': 'Rajasthan', 'Sikkim': 'Sikkim', 'Telangana': 'Telangana', 'TamilNadu': 'Tamil Nadu', 'Tripura': 'Tripura', 'UttarPradesh': 'Uttar Pradesh', 'Uttarakhand': 'Uttarakhand', 'WestBengal': 'West Bengal'}
    state = state_dict[state]
    add_user(name,code,number,state,district)
    

    return render_template('suc.html',
                            name=name,
                            code=code,
                            number=number,
                            state=state,
                            district=district)


port = int(os.getenv("PORT"))
if __name__ == '__main__':
    
    install()
    #print(os.getcwd())

    app.run(host='0.0.0.0',port=port)
    #app.run(debug=True)

    
