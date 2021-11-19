-- SQLite, SORT BY WEATHER TEMP
SELECT id, name, address, lat, long, weather_desc, weather_temp, wind
FROM locations 
ORDER BY weather_temp DESC;