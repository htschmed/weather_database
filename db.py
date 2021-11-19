import sqlite3
from sqlite3 import Error
from mapping import Location

class LocationDatabase:

    def __init__(self, file_path):
        self.create_connection(file_path)

    #Create Database and Setup a connection to the file
    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        self.conn = conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.conn.row_factory = sqlite3.Row
            self.create_location_table()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    #Close the database connection
    def close_connection(self):
        self.conn.close()

    #Create location table in database
    def create_location_table(self):
        create_sql = ''
        with open('location_tbl.sql', 'r') as sql_fptr:
            create_sql = sql_fptr.read()

        try:
            cursor = self.conn.cursor()
            cursor.execute(create_sql)
        except Error as e:
            print(e)

    #Insert database row using a Location Object
    def insert_location(self, location_obj):
        
        sql = '''
                INSERT INTO locations(name, address, lat, long, weather_desc, weather_temp, weather_unit, wind)
                VALUES(?,?,?,?,?,?,?,?)
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, [
                    location_obj.name,
                    location_obj.address,
                    location_obj.lat,
                    location_obj.long,
                    location_obj.weather_desc,
                    location_obj.temp,
                    location_obj.temp_unit,
                    location_obj.wind_direction + ' ' + location_obj.wind_speed
                ]
            )
            self.conn.commit()
            
        except Error as e:
            print(e)

    #Get location data from database rows using SQL Query
    def get_locations(self, sql='SELECT * FROM locations'):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            #return a name/vale dictionary for each row in the database
            return [dict(zip([c[0] for c in cursor.description], row)) for row in rows]
        except Error as e:
            print(e)

    #Update Location column/value
    def update_location(self, id, column_name, column_value):
        sql = f'UPDATE locations SET {column_name} = ? WHERE id = ?'
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, [column_value, id])
            self.conn.commit()
        except Error as e:
            print(e)

    #Delete row from database
    def delete_location(self, id):
        sql = '''
                DELETE FROM locations
                WHERE id = ?
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, [id]
            )
            self.conn.commit()
            
        except Error as e:
            print(e)
