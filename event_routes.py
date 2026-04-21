import os
from flask import Blueprint, render_template
import sqlite3
event_bp = Blueprint('event', __name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'campusconnect.db')
DB_PATH = os.path.abspath(DB_PATH)  # Ensures full absolute path
#Import CampusEventScraper class
from utils.event_scraper import CampusEventScraper

@event_bp.route("/events")
def events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, location, date FROM events")
    internal_events = cursor.fetchall()
    print(internal_events)

    #Creates an instance and runs the CampusEventScraper class
    scraper = CampusEventScraper()
    scraper.run()
    #Queries external_events table for scraped event data and fetches all event data
    cursor.execute("SELECT title, date, location, description FROM external_events")
    external_events = cursor.fetchall()
    

    conn.close()
    return render_template("events.html", internal_events=internal_events, external_events=external_events)