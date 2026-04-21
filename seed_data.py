import sqlite3
import os

DB_PATH = "db/campusconnect.db"

# Remove existing DB for a clean seed (optional in dev environment)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

#Opens, reads, and runs schema.sql
with open("db/schema.sql", "r") as f:
    sql = f.read()
    c.executescript(sql)

# Create tables manually or run schema.sql separately if preferred
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    preferences TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT
)''')

# Create Users Seed Data
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Alice", "Aly"))
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Bob", "art, Bobby"))
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Charlie", "Chaz"))

# Internal Events Seed Data
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Music Night", "Student Center", "2025-04-05"))
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Hackathon", "Library", "2025-04-01"))
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Art Exhibition", "Gallery", "2025-04-10"))
c.execute("SELECT title, location, date FROM events")

#External Events Seed Data
c.execute("""
INSERT INTO external_events(title, date, location, description) 
VALUES (?, ?, ?, ?)
     """,(
         "Career Fair",  
         "April 25 from 6:00 pm - 7:00pm", 
         "Merillat Sports & Fitness Center",
         "Come meet with potential employers!"
))

#API Seed Data
c.execute("""
INSERT INTO api_data(location, temperature, condition, humidity, wind_speed, precipitation, last_updated)
VALUES (?, ?, ?, ?, ?, ?, ?)
""",(
    "Adrian, MI",
    62.0,
    "Sunny",
    75,
    4.5,
    0.0,
    "2026-04-16"
))

conn.commit()
conn.close()