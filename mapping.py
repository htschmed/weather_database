import csv, codecs, requests
import numpy as np
from geopy.geocoders import Nominatim
from termcolor import colored


class Location:

    def __init__(self, name, address):
        
        #Initialize attributes
        self.name = name
        self.address = address
        self.lat = 0
        self.long = 0
        self._location = None

        #Initilize geolocater and get location by address
        geolocator = Nominatim(user_agent='OOP-Class')
        self._location = geolocator.geocode(self.address)
        
        #Set the Lat/Long attributes
        self.lat = self._location.latitude
        self.long = self._location.longitude

        #set weather data to blank
        self.weather_desc = None
        self.temp = None
        self.temp_unit = None
        self.wind_direction = None
        self.wind_speed = None

        #get the weather data and set it to the object attrs
        self.get_current_weather()

    def get_hourly_forecast(self):
        forecast_data = None
        
        # Add exception handling for not finding weather forecast data
        try:
            point_data_request = requests.get(f'https://api.weather.gov/points/{self.lat},{self.long}')
            point_data = point_data_request.json()
            forcast_hourly_url = point_data['properties']['forecastHourly']
            forecast_request = requests.get(forcast_hourly_url)
            forecast_data = forecast_request.json()['properties']['periods']
        except Exception as e:
            print(colored('Error: Could not retrieve forecast data', 'red'))
            print(colored(f'Reason: {e.__doc__}: {e}', 'red'))

        return forecast_data
    
    def get_current_weather(self):
        forecast_data = self.get_hourly_forecast()
        if forecast_data is not None and len(forecast_data) > 0:
            forecast = forecast_data[0]
            self.weather_desc = forecast['shortForecast']
            self.temp = forecast['temperature']
            self.temp_unit = forecast['temperatureUnit']
            self.wind_direction = forecast['windDirection']
            self.wind_speed = forecast['windSpeed']


    def __str__(self):
        return_str = '\n'
        return_str += f'Name: {self.name}\n'
        return_str += (f'Address: {self.address} \n')
        return_str += (f'Latitutude: {self.lat} \n')
        return_str += (f'Longitude: {self.long} \n\n')
        return_str += 'Weather Forecast: \n'
        return_str += f'Desc: {self.weather_desc}\n'
        return_str += f'Temp: {self.temp} {self.temp_unit}\n'
        return_str += f'Wind: {self.wind_direction} {self.wind_speed}'

        return return_str
    
    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'lat': self.lat,
            'long': self.long,
            'weather_desc': self.weather_desc,
            'temp': self.temp,
            'temp_unit': self.temp_unit,
            'wind_direction': self.wind_direction,
            'wind_speed': self.wind_speed,
        }
    
    def import_locations(filepath, delimiter=',', codec='utf-8'):
        locations_list = []
        with codecs.open(filepath, 'r', codec) as data_file:
            data_reader = csv.DictReader(data_file, delimiter=delimiter, quotechar='"')
            for row in data_reader:
                try:
                    location = Location(row['Name'], row['Address'])
                    locations_list.append(location)
                except Exception as e:
                    print(e)
                    print(row['Name'])
                    print(row['Address'])
        return locations_list


    def export_locations(location_list, filepath, delimiter=',', codec='utf-8'):
        
        with codecs.open(filepath, 'w', codec) as data_file:
            fieldnames = ['Name', 'Address', 'Latitude', 'Longitude', 'Current Weather']
            writer = csv.DictWriter(data_file, fieldnames=fieldnames, delimiter=delimiter)

            writer.writeheader()

            for x in location_list:
                forecast = x.get_current_weather()
                weather_desc = forecast['shortForecast']
                temperature = str(forecast['temperature']) + ' ' + forecast['temperatureUnit']
                wind_desc = forecast['windSpeed'] + ' ' + forecast['windDirection']
                writer.writerow(
                    {
                        'Name': x.name,
                        'Address': x.address,
                        'Latitude': x.lat,
                        'Longitude': x.long,
                        'Current Weather': f'{weather_desc};  {temperature};  Wind: {wind_desc}'
                    }
                )

def lat_long_to_mercator(lat, long):
    k = 6378137
    x = long * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k

    return {'x': x, 'y': y}