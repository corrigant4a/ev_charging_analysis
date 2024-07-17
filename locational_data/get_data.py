from pandas import read_csv, read_excel



j40_data = read_csv('locational_data/Justice40/j40_data.csv')
housing_data = read_csv('locational_data/Community_Survey/Survey_Data.csv')

dot_ddict = read_excel('locational_data/DOT_data/DataDictionary.xlsx')
dot_data = read_csv('locational_data/DOT_data/DOT_INDEX_5_3.csv')