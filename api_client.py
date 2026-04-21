import requests
import sqlite3

#Define a class to fetch and store weather data from an authenticated API
class WeatherAPI:
    """
    A class for getting weather data from Weather API and storing in the api_data table.

    Attributes:
        api_key (str): API key used to authenticate requests to Weather API.
        base_url (str): URL used to retrieve current weather data.
        conn (sqlite3.connect): Forms connection to sqlite database.
        cursor (sqlite3.cursor): Creates cursor to execute SQL commands

    Methods:
        fetch_weather (location): Gets current weather data for Adrian, MI.
        save_weather (weather): Saves weather data in api_data table.
        run (): Runs workflow of getting and storing weather data.
    """
    #Define constructor and store API key and base url, connect to database, and create cursor to execute SQL commands
    #Used ChatGPT to help with API base url, parameters, and troubleshooting rendering issues
    #Added page formatting with ChatGPT to api.html to render api data on /api webpage
    def __init__(self):
        """
        Acts as a constructor for the WeatherAPI object, setting API credentials, defining the base URL,
        and creating a database connection.
        """
        self.api_key = "50f84bb0155f4be6a69161928261204"
        self.base_url = "http://api.weatherapi.com/v1/current.json"
        self.conn = sqlite3.connect("db/campusconnect.db")
        self.cursor = self.conn.cursor()
    #Define a method to fetch weather for Adrian, MI and define parameters
    def fetch_weather(self, location="Adrian, MI"):
        """
        Gets current weather data for Adrian, MI using Weather API.

        Args:
            location (str): Specifies the location to retrieve data for and defaults to Adrian, MI.
        
        Returns:
            dict or None: A dictionary including weather data on location, temperature, condition,
            humidity, wind speed, precipitation, and last updated time. Returns None if API response
            is invalid.
        """
        params = {
            "key": self.api_key,
            "q": location,
            "aqi": "no"
        }
        #Send get request to weather api with query parameters
        response = requests.get(self.base_url, params=params)
        #Parse json
        data = response.json()
        #Checks that weather data is valid
        if "location" not in data:
            print("ERROR RESPONSE:", data)
            return None
        #Extracts data from API response
        weather = {
            "location": data["location"]["name"],
            "temperature": data["current"]["temp_f"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind_speed": data["current"]["wind_mph"],
            "precipitation": data["current"]["precip_in"],
            "last_updated": data["current"]["last_updated"]
        }
        #Returns dictionary of weather data
        return weather
    #Define a method to save weather or exit function if there is no weather data
    def save_weather(self, weather):
        """
        Saves weather into sqlite database.

        Args:
            weather (dict): A dictionary containing weather data returned from fetch_weather().

        Returns:
            None.
        """
        if not weather:
            return
        #Insert weather data into api_data table
        self.cursor.execute("""
            INSERT INTO api_data 
            (location, temperature, condition, humidity, wind_speed, precipitation, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            weather["location"],
            weather["temperature"],
            weather["condition"],
            weather["humidity"],
            weather["wind_speed"],
            weather["precipitation"],
            weather["last_updated"]
        ))
        #Save database changes
        self.conn.commit()
    #Define a method to run workflow and fetch and store api data
    def run(self):
        """
        Runs full workflow by getting weather information and storing valid data in database.

        Returns:
            dict or None: Returns a dictionary of retrieved weather data if successful, otherwise returns None.
        """
        print("API RUNNING")
        weather = self.fetch_weather()

        if weather:
            self.save_weather(weather)
        #Returns weather data
        return weather
