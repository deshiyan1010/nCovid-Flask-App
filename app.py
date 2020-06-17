from flask import Flask, render_template, request
from plot import plot
import plotly
import os


app = Flask(__name__,static_url_path='/static')

def mon_name_num(month):
    mon_dict = {"January":1,"February":2,"March":3,
              "April":4,"May":5,"June":6,"July":7,
              "August":8,"September":9,"October":10,
              "November":11,"December":12}
    return mon_dict[month]

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
    states = ["Total India","Andaman and Nicobar Islands","Andra Pradesh",
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
    months = ["January","February","March",
              "April","May","June","July",
              "August","September","October",
              "November","December"]
    dates = [str(x) for x in range(1,32)]
    years = ["2020","2021"]
    types = ["Confirmed","Recovered","Deceased"]
    cum_das = ["Cumulative","Daily"]
    return render_template('index.html',states=states,
                           months=months,
                           dates=dates,
                           years=years,
                           types=types,
                           cum_das=cum_das)

@app.route('/math', methods=['POST'])  # This will be called from UI
def math_operation():
    if (request.method=='POST'):
        sttNM = request.form['state']
        statex = state_code(sttNM)
        #month = mon_name_num(request.form['month'])
        #date = request.form['date']
        #year = request.form['year']
        typex = request.form['type']
        datex = request.form['datex']
        cum_dax = request.form['cum_da']
        #data =plot(cat=str(typex),state=state,till=str(year)+"-"+str(month)+"-"+str(date))
        data =plot(cat=str(typex),state=statex,till=str(datex),cum_da=str(cum_dax),stt_name=sttNM)

        #graphJSON = json.dumps(data,cls=plotly.utils.PlotlyJSONEncoder)

        #num1=int(request.form['num1'])
        #num2 = int(request.form['num2'])

        return render_template('file.html')#,graphJSON=graphJSON


#port = int(os.getenv("PORT"))
if __name__ == '__main__':
    
    #print(os.getcwd())
    try:
        path = os.path.join(os.getcwd(),"templates","file.html")
        os.remove(path)
    except:
        print("nope")
        pass
    #app.run(host='0.0.0.0',port=port)
    app.run(debug=True)