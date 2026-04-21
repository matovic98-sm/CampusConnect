from flask import Blueprint, render_template
#Import WeatherAPI class
from utils.api_client import WeatherAPI
import sqlite3
api_bp = Blueprint('api', __name__)

@api_bp.route("/api")
def api():
    conn = sqlite3.connect("db/campusconnect.db")
    cursor = conn.cursor()
    #Create an instance of WeatherAPI class to use and run public API
    api_client = WeatherAPI()
    api_client.run()
    #Select weather from api_data table, order by newest entry, and limit to most recent weather
    #Used ChatGPT to only display current weather data
    cursor.execute("""
        SELECT location, temperature, condition, humidity, wind_speed, precipitation, last_updated
        FROM api_data
        ORDER BY id DESC
        LIMIT 1
    """)
    #Fetch most recent weather data
    api_data = cursor.fetchone()
    conn.close()

    return render_template("api.html", api_data=api_data)

