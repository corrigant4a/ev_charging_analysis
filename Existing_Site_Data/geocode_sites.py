# %%
import pandas as pd 
from pygris.geocode import geocode as pygeocode
from osmnx.geocoder import geocode as oxgeocode
from math import isnan

# %%
raw_data = pd.read_csv('Existing_Site_Data/NEVI Project Site Locations - 5_23_24 Update.csv')

try:
    loc_data = pd.read_csv('Existing_Site_Data/site_coords.csv', delimiter = ';')
    print(f'Site Data found for {len(loc_data)}/{len(raw_data)} locations')
except FileNotFoundError:
    loc_data = pd.DataFrame(columns = ['Address', 'Latitude', 'Longitude'])
    print('Site data not found')




# %%
for i, address in enumerate(raw_data['Address']):

    if address not in loc_data['Address'].values:
        
        try:
            coord = pygeocode(address)
            print(coord)
            loc_data.loc[len(loc_data)] = {'Address': address, 'Latitude': coord.Latitude, 'Longitude': coord.Longitude}

        except:
            try:
                coord = oxgeocode(address)
                print(coord)
                loc_data.loc[len(loc_data)] = {'Address': address, 'Latitude': coord[0], 'Longitude': coord[1]}

            except:
                print('Could not geocode address')
                print(f'Addess: {address}')
                loc_data.loc[len(loc_data)] = {'Address': address, 'Latitude': None, 'Longitude': None}




# %%
loc_data.to_csv('Existing_Site_Data/site_coords.csv', sep = ';', columns= ['Address', 'Latitude', 'Longitude'], index = False)



