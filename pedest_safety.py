import osmnx as ox
import numpy as np

highway_types = ['residential', 'trunk', 'motorway', 'primary', 'secondary', 'tertiary', 'unclassified', 'service', 'road', "living_street"]
highway_speeds = {"motorway": 65, "trunk": 50, "primary": 50, "secondary": 40, "tertiary": 40, "unclassified": 40, "residential": 25, "living_street": 20, "service": 25, "road": 30, "unclassified": 30} #in mph

for way_type in highway_types[:7]:
    highway_types.append(way_type + '_link')
    highway_speeds[way_type + '_link'] = highway_speeds[way_type]


fatal_like_speed_data = np.array([[16, 23, 31, 39, 46], [0.1, 0.25, 0.5, 0.75, 0.9]])
fatal_like_speed = lambda x: np.interp(x, fatal_like_speed_data[0], fatal_like_speed_data[1])


def safety_info(location):
    try:
        nodes = ox.features.features_from_point(center_point= location, dist = 100, tags = {"highway": highway_types})

        if 'maxspeed' in nodes.keys():
            max_speed = int(max(nodes['maxspeed']))

        else:

            speeds = [highway_speeds[hi_ty] for hi_ty in nodes["highway"]]
            max_speed = max(speeds)
        
        return max_speed, fatal_like_speed(max_speed)

    except:
        max_speed = None   
        return None, None

    