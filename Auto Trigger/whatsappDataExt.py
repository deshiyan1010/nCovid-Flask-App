from statewise import get_table_cum,get_table_daily
import pandas as pd 
from districtData import districtwise_info,district_to_daywise

def data(state,district):

    #Cum
    table1,table2,table3,table4 = get_table_cum()
    state_table = pd.concat([table1,table2,table3,table4],axis=1)

    district_table = pd.DataFrame(districtwise_info(state))

    state_table.columns = ["State","Confirmed","Recovered","Deceased"]
    district_table.columns = ["District","Confirmed","Active","Recovered","Deceased"]
    state_data_cum = state_table.loc[state_table["State"] == state]
    district_data_cum = district_table.loc[district_table["District"] == district]

    india_data_cum = state_table.loc[state_table["State"]=="Total India"]

    
   

    #Daily

    table1,table2,table3,table4 = get_table_daily()
    
    state_table = pd.concat([table1,table2,table3,table4],axis=1)
    
    district_table = district_to_daywise()
    
    state_table.columns = ["State","Confirmed","Recovered","Deceased"]
    district_table.columns = ["District","Confirmed","Active","Recovered","Deceased"]
    state_data_daily = state_table.loc[state_table["State"] == state]
    district_data_daily = district_table.loc[district_table["District"] == district]

    india_data_daily = state_table.loc[state_table["State"]=="Total India"]

    
    
    return india_data_cum,state_data_cum,district_data_cum,india_data_daily,state_data_daily,district_data_daily


if __name__=="__main__":
    wamain(1,1,"Karnataka","Mysuru")