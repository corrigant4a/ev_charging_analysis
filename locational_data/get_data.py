from pandas import read_csv, read_excel



j40_data = read_csv('locational_data/Justice40/j40_data.csv')
housing_data = read_csv('locational_data/Community_Survey/Survey_Data.csv')
lead_data = read_csv('locational_data/LEAD_tool_data/LEAD Tool Data Census Tracts.csv')

dot_ddict = read_excel('locational_data/DOT_data/DataDictionary.xlsx')

try:
    dot_data = read_csv('locational_data/DOT_data/DOT_INDEX_5_3.csv')
except:
    print('DOT data not found. File is too large to be included, so user must use local version of file. File can be found at site https://www.transportation.gov/priorities/equity/justice40/download-data')
    dot_data = None