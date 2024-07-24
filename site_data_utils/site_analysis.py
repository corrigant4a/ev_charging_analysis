import osmnx as ox
import pandas as pd

from site_data_utils.nearby_amenities import find_nearby_poi
from site_data_utils.pedest_safety import safety_info
from site_data_utils.data_process import census_tract_data
from site_data_utils.find_charging import find_ev_charging

ox.settings.log_console = True

from global_params import *



def get_info(location, output = "DataFrame", debug = False):

    """location: coords as (lat, long)
    output: either 'DataFrame' or 'JSON', specifies return format for data 
    debug: boolean whether to do in debug mode"""

    if output != 'DataFrame' and output != 'JSON':
        raise Exception('output argument must be "DataFrame" or "JSON"')

    G = ox.graph_from_point(center_point = location, dist = WALK_DIST, network_type= 'walk')
    #creates osmnx graph of nearby walking network

    tract_data = census_tract_data(location, debug = debug)

    loc_safety_info = safety_info(location, debug = debug)

    nearby_poi = find_nearby_poi(G, location, walking_distance = WALK_DIST, debug = debug)
    
    nearby_charging_sites = find_ev_charging(G, location, walking_distance = WALK_DIST, debug = debug)
    #gets all relevant data from each function

    data_frame = pd.concat([tract_data, loc_safety_info, nearby_poi, nearby_charging_sites])

    if output == "DataFrame":
        return data_frame
    elif output == "JSON":
        return data_frame.to_json()