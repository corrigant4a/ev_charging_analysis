import csv

api_keys = {}
with open('api_files/api_keys.csv', 'r') as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        api_keys[line[0]] = line[1].replace(' ','')

nrel_key = api_keys['NREL_API']