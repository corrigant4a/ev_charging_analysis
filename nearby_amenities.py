import osmnx as ox

relevant_amenities = ['restaurant', 'pub', 'bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'library', 'atm', 'bank', 'money_transfer', 'payment_center', 'bureau_de_change', 'payment terminal', 'pharmacy', 'arts_centre', 'cinema', 'community_centre', 'planetarium']
relevant_buildings = ['retail', 'supermarket', 'museum', 'sports_centre', 'sports_hall', 'riding_hall', 'pavilion', 'stadium']
relevant_tourism = ['artwork', 'attraction', 'gallery', 'information', 'museum', 'picnic_site', 'viewpoint', 'zoo', ]


tags = {'amenity': relevant_buildings,
        'building': relevant_amenities,
        'tourism': relevant_tourism}


def num_nearby_amenities(location, walking_distance = 500, tags = tags):

    try: 
            gdf = ox.features.features_from_point(location, dist=walking_distance, tags=tags)
            num_amenities_euc = len(gdf)

            num_amenities = 0
            G = ox.graph_from_point(center_point = location, dist = walking_distance, network_type= 'walk')

            for i in range(num_amenities_euc):
                    query = f'{gdf["addr:housenumber"].iloc[i]} {gdf["addr:street"].iloc[i]}, {gdf["addr:city"].iloc[i]} {gdf["addr:state"].iloc[i]}, {gdf["addr:postcode"].iloc[i]} '

                    amenity_loc  = ox.geocoder.geocode(query)

                    node1, dist1 = ox.distance.nearest_nodes(G, X = location[1], Y = location[0], return_dist = True)
                    node2, dist2 = ox.distance.nearest_nodes(G, X = amenity_loc[1], Y = amenity_loc[0], return_dist = True)

                    route = ox.routing.shortest_path(G, node1, node2, weight='length', cpus=1)
                    edges = ox.routing.route_to_gdf(G, route, weight = 'length')

                    total_dist = dist1 + sum(edges['length']) + dist2

                    if total_dist < walking_distance:
                            num_amenities += 1
                    

    except:
            num_amenities = 0


    return num_amenities