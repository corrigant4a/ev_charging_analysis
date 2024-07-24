import osmnx as ox
import pandas as pd
from global_params import *



relevant_amenities = ['restaurant', 'pub', 'bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'library', 'atm', 'bank', 'money_transfer', 'payment_center', 'bureau_de_change', 'payment terminal', 'pharmacy', 'arts_centre', 'cinema', 'community_centre', 'planetarium']
relevant_buildings = ['retail', 'supermarket', 'museum', 'sports_centre', 'sports_hall', 'riding_hall', 'pavilion', 'stadium']
relevant_tourism = ['artwork', 'attraction', 'gallery', 'information', 'museum', 'picnic_site', 'viewpoint', 'zoo', ]


amenity_tags = {'amenity': relevant_amenities,
        'building': relevant_buildings,
        'tourism': relevant_tourism}

# ev_tags = {'amenity': ["charging_station"]}

bus_stop_tags = {'highway': ['bus_stop', 'bus_bay'], 'amenity': ['bus_station']}

bike_rental_tags = {'amenity': ['bicycle_rental']}

subway_tags = {'station': 'subway'}

tags = {"amenities": amenity_tags,
        "bus stops": bus_stop_tags, "bike rentals": bike_rental_tags, "subway stations": subway_tags}



def test_walking_distance(G, location, test_loc, walking_distance, debug = False):

    """G: graph
    location: coords in (lat, long) format
    test_loc: coords of secondary location as (lat, long)
    walking_distance: max allowed walking distance
    
    returns True if network walking distance is <= walking_distance, False otherwise """


    if ox.distance.great_circle(lat1 = location[0], lon1 = location[1], lat2 = test_loc[0], lon2 = test_loc[1]) < 50:
         return True
    #if the distance is very short there may be no actual walking path between the nodes even though it is walkable. 


    node1, dist1 = ox.distance.nearest_nodes(G, X = location[1], Y = location[0], return_dist = True)
    node2, dist2 = ox.distance.nearest_nodes(G, X = test_loc[1], Y = test_loc[0], return_dist = True)

    if debug:
         def pick_color(node_id):
              if node_id == node1:
                   return 'red'
              elif node_id == node2:
                   return 'green'
              return 'black'
         
         ox.plot_graph(G, node_color=[pick_color(node) for node in G.nodes])
         print(f'node1 {node1} \n node2 {node2}')
    
    if node1 == node2:
         return True
    #if both locations are the same node the walking time is minimal
    
    route = ox.routing.shortest_path(G, node1, node2, weight='length', cpus=1)
    edges = ox.routing.route_to_gdf(G, route, weight = 'length')

    total_dist = dist1 + sum(edges['length']) + dist2

    return total_dist <= walking_distance
       

def find_nearby_poi(G, location, walking_distance = 500, tags = tags, debug = False):
    """
    
    location: is the latitude, longitude of the target location
    
    walking_distance: is the allowed distance to walk in meters
    
    tags: is a dictionary of types of points of interest as keys (poi) 
    with the values as further dictionaries 
    Those subdictionaries have osmnx tags as keys and lists of instances 
    of those tags as values

    returns a pd Sereies with type of point of interest as keys and number of relevant locations as values"""
    
    points_of_interest = {}


    for key, value in tags.items():
        try: 
                gdf = ox.features.features_from_point(location, dist=walking_distance, tags=value)


                num_amenities_euc = len(gdf)

                num_poi = 0

                for i in range(num_amenities_euc):
                    query = f'{gdf["addr:housenumber"].iloc[i]} {gdf["addr:street"].iloc[i]}, {gdf["addr:city"].iloc[i]} {gdf["addr:state"].iloc[i]}, {gdf["addr:postcode"].iloc[i]} '
                    amenity_loc  = ox.geocoder.geocode(query)
                    num_poi += test_walking_distance(G, location=location, amenity_loc= amenity_loc, walking_distance = walking_distance, debug = debug)
                        

        except:
                num_poi = 0

        points_of_interest[key] = num_poi


    return pd.concat([pd.Series(points_of_interest)])





