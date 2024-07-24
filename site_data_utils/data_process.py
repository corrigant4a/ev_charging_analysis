
from pygris.geocode import geolookup
import pandas as pd
import numpy as np
from site_data_utils.locational_data.get_data import j40_data, housing_data, dot_data, lead_data


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

relev_lead_fields = [r"Energy Burden (% income)","Avg. Annual Energy Cost ($)","Total Households","Household Income"]

relev_dot_data_fields_dict = {}

dot_data_not_found_message = 'File is too large to be included, so user must use local version of file. File can be found at site https://www.transportation.gov/priorities/equity/justice40/download-data'


def make_dot_key_dict():
    key_dict = {}
    for i, line in enumerate(relev_dot_data_fields.split('\n')):
        if i%2 == 0:
            key = line 
        else:
            val = line[6:]
            key_dict[key] = val
    return key_dict

dot_key_dict = make_dot_key_dict()

cond_housing_data = pd.DataFrame({"Number People in Census Tract": housing_data["Estimate!!Total:"], "Single Dwelling Home": housing_data.iloc[:,4:8:2].sum(axis = 1), "2+ Dwelling or Unconventional Home": housing_data.iloc[:,8:-1:2].sum(axis = 1)})


def get_census_num(location):
    """location: Inputs the location at (lat, long)
    outputs the census tract number
    the geolookup gives a longer number with more information than is necessary"""
    return int(geolookup(location[1], location[0])['GEOID'][0][:11])

def row_num(dataset, census_id_key, census_num):
    """dataset: is the DataFrame with all the information in it
    census_id_key: is the key for dataset that gives the cencus tract number
    census_num: is the census number being queried
    returns the row index of dataset that contains the information of the given census_num"""
    try:
        return np.argwhere(dataset[census_id_key].values == census_num)[0,0]
    except IndexError:
        return None



def get_info(census_num, dataset, census_id_key, relevant_data_fields, data_cat = None, special_message = None, key_dict = None, census_num_formatter = lambda n: n):
    """
    census_num: census tract number of queried location, integer type
    dataset: the dataset being queried, stored as pd dataFrame
    census_id_key: the key in the dataFrame dataset that corresponds to the census tract numbers, type is string
    relevant_data_fields: A Python list of strings of the keys in dataset that correspond to relevant data fields. Must be (not necessarily proper) subset of dataset.keys()
    data_cat: a string describing the data category
    special_message: A message to return if the dataset is not found, type is string
    key_dict: A dictionary used to translate the dataset keys to a human readable format, if necessary, the keys are the human readable values and the values are the keys used in the original dataset. Both keys and values are strings 
    census_num_formatter: a function that takes in the census_num (integer) and outputs the formatted value that is stored in the desired dataset"""

    if dataset is None:
        print(f'{data_cat} data not found. {special_message}')
        return pd.Series({key: None for key, _ in relevant_data_fields})

    row = row_num(dataset, census_id_key, census_num_formatter(census_num))

    if row is None:
        return pd.Series({key: None for key in dataset.keys()})
    #if row is num it means the census tract couldn't be found in the dataset

    coded_data = dataset[relevant_data_fields].iloc[row]

    if key_dict is None:
        return coded_data

    return pd.Series({key: coded_data[value] for key, value in key_dict.items()})



dot_data_args = {'dataset': dot_data, 'census_id_key': 'trctfp', 'relevant_data_fields': dot_key_dict.values(), 'data_cat': 'DOT data', 'special_message': dot_data_not_found_message, 'key_dict': dot_key_dict}

lead_data_args = {'dataset': lead_data, 'census_id_key': "Geography ID", 'relevant_data_fields': relev_lead_fields, 'data_cat': 'LEAD data'}

j40_data_args = {'dataset': j40_data, 'census_id_key': 'Census tract 2010 ID', 'relevant_data_fields': relev_j40_disad, 'data_cat': 'Justice40 data'}

housing_data_args = {'dataset': housing_data, 'census_id_key': 'Geography', 'relevant_data_fields': housing_data.keys(), 'data_cat': 'Housing data', 'census_num_formatter': (lambda n: f"1400000US{n}")}

data_cats = [dot_data_args, lead_data_args, j40_data_args, housing_data_args]

def census_tract_data(location, debug = False):
    """takes location and returns all the relevant information as a DataFrame"""
    census_num = get_census_num(location)

    return pd.concat([get_info(census_num=census_num, **args) for args in data_cats])
