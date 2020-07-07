from plot_single import get_table
import pandas as pd 
from districtData import districtwise_info

def data(state,district):

    table1,table2,table3,table4 = get_table()
    state_table = pd.concat([table1,table2,table3,table4],axis=1)

    district_table = pd.DataFrame(districtwise_info(state))

    state_table.columns = ["State","Confirmed","Recovered","Deceased"]
    district_table.columns = ["District","Confirmed","Active","Recovered","Deceased"]
    state_data = state_table.loc[state_table["State"] == state]
    district_data = district_table.loc[district_table["District"] == district]

    india_data = state_table.loc[state_table["State"]=="Total India"]


    return india_data,state_data,district_data


if __name__=="__main__":
    wamain(1,1,"Karnataka","Mysuru")