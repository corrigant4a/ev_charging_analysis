
from pygris.geocode import geolookup
import pandas as pd
import numpy as np
from locational_data.get_data import j40_data, housing_data, dot_data, dot_ddict


relev_j40_disad = """PM2.5 in the air (percentile)
PM2.5 in the air
Diesel particulate matter exposure (percentile)
Diesel particulate matter exposure
Traffic proximity and volume (percentile)
Traffic proximity and volume
DOT Travel Barriers Score (percentile)
Greater than or equal to the 90th percentile for housing burden and is low income?
Tract experienced historic underinvestment and remains low income
Tract experienced historic underinvestment""".split('\n')

relev_dot_data_fields = """Income of surrounding areas
Code: hhminc
Estimated cost of transportation
Code: estct
Cost burden for transportation
Code: avghht
Proportion of households without vehicles
Code: pctnvh
Walk times to…Adult Education
Code: wtae
Grocery Stores
Code: wtgs
Medical Facilities
Code: wtmf
Parks
Code: wtp
Primary Schools
Code: wtps
Drive times to…Adult Education
Code: dtae
Grocery Stores
Code: dtgs
Medical Facilities
Code: dtmf
Parks
Code: dtp
Primary Schools
Code: dtps
Traffic fatalities per 100,000 people
Code: ftltsp"""

relev_dot_data_fields_dict = {}

for i, line in enumerate(relev_dot_data_fields.split('\n')):
    if i%2 == 0:
        key = line 
    else:
        val = line[6:]
        relev_dot_data_fields_dict[key] = val

def get_census_num(location):
    return int(geolookup(location[1], location[0])['GEOID'][0][:11])


def get_dot_info(location):
    row = np.argwhere(dot_data['trctfp'].values == get_census_num(location))[0,0]
    coded_dot_data = dot_data[relev_dot_data_fields_dict.values()].iloc[row]
    return pd.Series({key: coded_dot_data[value] for key, value in relev_dot_data_fields_dict.items()})




cond_housing_data = pd.DataFrame({"Number People in Census Tract": housing_data["Estimate!!Total:"], "Single Dwelling Home": housing_data.iloc[:,4:8:2].sum(axis = 1), "2+ Dwelling or Unconventional Home": housing_data.iloc[:,8:-1:2].sum(axis = 1)})



def get_j40_info(location):
    row = np.argwhere(j40_data['Census tract 2010 ID'].values == get_census_num(location))[0,0]
    return j40_data[relev_j40_disad].iloc[row]

def get_housing_info(location):
    row = np.argwhere(housing_data['Geography'].values == f"1400000US{get_census_num(location)}")[0,0]
    return cond_housing_data.iloc[row]

def census_tract_data(location):
    if get_census_num(location) in j40_data['Census tract 2010 ID'].values:
        return pd.concat([pd.Series({'Location in Census Tract': True}), get_j40_info(location), get_housing_info(location), get_dot_info(location)])
    return pd.Series({'Location in Census Tract': False})
