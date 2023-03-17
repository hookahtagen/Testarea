import json

import requests
import urllib.parse
from unix_to_realtime import unix_to_realtime


class WeatherSystem:

    def __init__(self, name: str):
        self.name = name
        self.api_key = ""
        self.lat = 0.0
        self.long = 0.0
        self.url = ""
        self.country_code = {
            "Germany": "de",
            "United States": "us",
            "United Kingdom": "gb",
            "France": "fr",
            "Italy": "it",
            "Spain": "es",
            "Poland": "pl",
            "Romania": "ro",
            "Netherlands": "nl",
            "Belgium": "be",
            "Greece": "gr",
            "Czechia": "cz",
            "Portugal": "pt",
            "Hungary": "hu",
            "Sweden": "se",
            "Austria": "at",
            "Bulgaria": "bg",
            "Switzerland": "ch",
            "Denmark": "dk",
            "Norway": "no"
        }

    @staticmethod
    def get_location_details(location: str):
        address = location.replace("ß", "ss")
        address = urllib.parse.quote(address)

        url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"

        response = requests.get(url).json()
        lat = response[0]["lat"]
        long = response[0]["lon"]

        # print(f"Cordinates for {location}: {lat}, {long}")

        return lat, long

    def get_weather(self, location: str):
        lat, long = self.get_location_details(location)

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={self.api_key}&units=metric"

        response = requests.get(url).json()

        # convert dt to a realtime timestamp
        response["dt"] = unix_to_realtime(response["dt"])
        response["sys"]["sunrise"] = unix_to_realtime(response["sys"]["sunrise"])
        response["sys"]["sunset"] = unix_to_realtime(response["sys"]["sunset"])
        country_c = response["sys"]["country"].lower()
        # convert country code to country name which is located in the country_code dict as key
        response["sys"]["country"] = list(self.country_code.keys())[list(self.country_code.values()).index(country_c)]

        # print the response with an indentation of 4
        received_data = json.dumps(response, indent=4)

        return received_data

    def get_temperature(self, location: str):
        weather_data = self.get_weather(location)
        weather_data = json.loads(weather_data)
        current_temp = weather_data["main"]["temp"]

        return current_temp


if __name__ == "__main__":
    location_address = "Bluddenstraße 5, Wadersloh, Germany"
    weather = WeatherSystem("Weather System")

    temperature = weather.get_temperature(location_address)
    print(f"The current temperature in {location_address} is {temperature}°C")
