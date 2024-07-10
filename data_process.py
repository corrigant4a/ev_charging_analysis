
from pygris.geocode import geolookup
import pandas as pd
import numpy as np



relev_disad = """PM2.5 in the air (percentile)
PM2.5 in the air
Diesel particulate matter exposure (percentile)
Diesel particulate matter exposure
Traffic proximity and volume (percentile)
Traffic proximity and volume
DOT Travel Barriers Score (percentile)
Greater than or equal to the 90th percentile for housing burden and is low income?
Tract experienced historic underinvestment and remains low income
Tract experienced historic underinvestment""".split('\n')

def get_census_num(location):
    return int(geolookup(location[1], location[0])['GEOID'][0][:11])


j40_data = pd.read_csv('j40_data.csv')
housing_data = pd.read_csv('Community_Survey/Survey_Data.csv')
# print(community_data.keys)
# 484299502001041 in community_data['Census tract 2010 ID'].values


cond_housing_data = pd.DataFrame({"Number People in Census Tract": housing_data["Estimate!!Total:"], "Single Dwelling Home": housing_data.iloc[:,4:8:2].sum(axis = 1), "2+ Dwelling or Unconventional Home": housing_data.iloc[:,8:-1:2].sum(axis = 1)})



def get_j40_info(location):
    row = np.argwhere(j40_data['Census tract 2010 ID'].values == get_census_num(location))[0,0]
    return j40_data[relev_disad].iloc[row]

def get_housing_info(location):
    row = np.argwhere(housing_data['Geography'].values == f"1400000US{get_census_num(location)}")[0,0]
    return cond_housing_data.iloc[row]

def census_tract_data(location):
    if get_census_num(location) in j40_data['Census tract 2010 ID'].values:
        return pd.concat([pd.Series({'Location in Census Tract': True}), get_j40_info(location), get_housing_info(location)])
    return pd.Series({'Location in Census Tract': False})
