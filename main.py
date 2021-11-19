import configparser
from db import LocationDatabase
from mapping import Location
from pprint import pprint

config = configparser.ConfigParser()
config.read('config.ini')

school_filepath = config['Data Files']['school_file']
db_filepath = config['Data Files']['db_file']

location_list = Location.import_locations(school_filepath, delimiter='\t', codec='utf-16')

#Initialize our SQLITE 
location_db = LocationDatabase(db_filepath)

#Insert location object data into SQLITE Database
for item in location_list:
    location_db.insert_location(item)

#Print out database rows
pprint(location_db.get_locations())

#Update one database row column/value
location_db.update_location(3, 'name', 'Updated Name')

pprint(location_db.get_locations())

#Delete database row
location_db.delete_location(2)

pprint(location_db.get_locations())