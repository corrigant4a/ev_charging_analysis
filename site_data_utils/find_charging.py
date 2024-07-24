import requests
from .nearby_amenities import test_walking_distance
from global_params import *
import pandas as pd

try:
    from api_files.api_keys import nrel_key




    def nrel_request(location, walking_distance):
        """location: coordinates in (lat, long) tuple
        walking_distance: allowed distance from location (in meters)
        returns NREL charging site data within walking_distance of location in JSON format"""
        request_params = {'api_key': nrel_key, 'fuel_type': 'ELEC', 'latitude': location[0], 'longitude': location[1], 'radius': walking_distance * MILES_PER_METER, 'limit': 50}

        return requests.get('https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?' + ''.join([f'{key}={value}&' for key, value in request_params.items()])).json()

    def find_ev_charging(G, location, walking_distance= WALK_DIST, debug = False):
        """G: graph
        location: coords as (lat, long)
        walking_distance: distance from location in meters
        returns numbers of stations of each type within walking_distance meters of location"""

        site_stats = {'Number of Stations': 0, 'ev_dc_fast_num': 0, 'ev_level1_evse_num': 0, 'ev_level2_evse_num': 0}

        charger_types = ['ev_dc_fast_num', 'ev_level1_evse_num', 'ev_level2_evse_num']

        response = nrel_request(location, walking_distance)

        for station in response['fuel_stations']:
            ev_loc = (station['latitude'], station['longitude'])

            if test_walking_distance(G, location, ev_loc, walking_distance, debug = debug):
                 #check that station is within network walking distance rather than
                 #Euclidean distance which is returned by the NREL API
                site_stats['Number of Stations'] += 1 

                for charge_type in charger_types:
                    site_stats[charge_type] += station[charge_type] if station[charge_type] else 0


        return pd.Series(site_stats)

except:
    print("API key not found. Need to add own csv file containing an NREL API key")
    def find_ev_charging(G, location, walking_distance= WALK_DIST):
        print("API key not found. Need to add own csv file containing an NREL API key")
        return pd.Series({})