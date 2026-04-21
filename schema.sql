-- SQLite schema
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    preferences TEXT
);

DROP TABLE IF EXISTS events;
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT
);

-- Create external scraped events table here
DROP TABLE IF EXISTS external_events;
CREATE TABLE external_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    date TEXT,
    location TEXT,
    description TEXT
);
--Create api data table
DROP TABLE IF EXISTS api_data;
CREATE TABLE api_data (
id INTEGER PRIMARY KEY AUTOINCREMENT,
location TEXT,
temperature REAL,
condition TEXT,
humidity INTEGER,
wind_speed REAL,
precipitation REAL,
last_updated TEXT
);
