# %%
import pandas as pd 
import osmnx as ox


# %%
raw_data = pd.read_csv('Existing_Site_Data/NEVI Project Site Locations - 5_23_24 Update.csv')

try:
    loc_data = pd.read_csv('Existing_Site_Data/site_coords.csv', delimiter = ';')
    print(f'Site Data found for {len(loc_data)}/{len(raw_data)} locations')
except:
    loc_data = pd.DataFrame(columns = ['Address', 'Latitude', 'Longitude'])
    print('Site data not found')




# %%
for i, address in enumerate(raw_data['Address']):

    if address not in loc_data['Address'].values:

        try:
            coord = ox.geocoder.geocode(address)
            print(coord)
            loc_data.loc[len(loc_data)] = {'Address': address, 'Latitude': coord[0], 'Longitude': coord[1]}

        except:
            print('Could not geocode address')
            loc_data.loc[len(loc_data)] = {'Address': address, 'Latitude': None, 'Longitude': None}




# %%
loc_data.to_csv('Existing_Site_Data/site_coords.csv', sep = ';', columns= ['Address', 'Latitude', 'Longitude'], index = False)



