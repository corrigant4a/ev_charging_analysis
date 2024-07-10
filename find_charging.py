import requests
from nearby_amenities import test_walking_distance
from global_params import *
from api_keys import nrel_key
import pandas as pd


def format_request(location):
    request_params = {'api_key': nrel_key, 'fuel_type': 'ELEC', 'latitude': location[0], 'longitude': location[1], 'radius': WALK_DIST_MILE, 'limit': 50}

    return 'https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?' + ''.join([f'{key}={value}&' for key, value in request_params.items()])

def find_ev_charging(G, location):

    site_stats = {'Number of Stations': 0, 'ev_dc_fast_num': 0, 'ev_level1_evse_num': 0, 'ev_level2_evse_num': 0}

    charger_types = ['ev_dc_fast_num', 'ev_level1_evse_num', 'ev_level2_evse_num']

    response = requests.get(format_request(location))

    for station in response.json()['fuel_stations']:
        ev_loc = (station['latitude'], station['longitude'])

        if test_walking_distance(G, location, ev_loc, WALK_DIST):
             site_stats['Number of Stations'] += 1 

             for charge_type in charger_types:
                  site_stats[charge_type] += station[charge_type] if station[charge_type] else 0


    return pd.Series(site_stats)