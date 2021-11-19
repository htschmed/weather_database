CREATE TABLE IF NOT EXISTS locations (
    id integer PRIMARY KEY,
    name text NOT NULL,
    address text NOT NULL,
    lat real,
    long real,
    weather_desc text,
    weather_temp int,
    weather_unit text,
    wind text
);