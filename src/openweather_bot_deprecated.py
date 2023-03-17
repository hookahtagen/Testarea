import time

import numpy as np
from datetime import datetime, timedelta, timezone
from sklearn.linear_model import LinearRegression


def wait_loop(wait_time: float):
    """
    This function takes a float as input. It serves as a wait loop for the given amount of time.
    If the wait time is greater than 1 minute, the remaining time is printed every 30 seconds.
    :param wait_time: float
    :return:
    """

    print(f"Waiting for {wait_time / 60:.1f} minutes...")

    # If wait time is greater than 1 minute, print remaining time every 30 seconds
    if wait_time > 60:
        while wait_time > 0:
            time.sleep(30)
            wait_time -= 30
            print(f"Remaining time: {wait_time / 60:.1f} minutes")

    # If wait time is less than 1 minute, sleep for the given amount of time
    else:
        print(f"Remaining time: {wait_time:.0f} seconds")
        time.sleep(wait_time)


# Create initial dataset
data = [
    (datetime.fromisoformat("2022-03-14T12:00:00+01:00").replace(tzinfo=timezone.utc), 23.5, 1013.2, 0.65, 5),
    (datetime.fromisoformat("2022-03-14T12:10:00+01:00").replace(tzinfo=timezone.utc), 23.6, 1013.1, 0.63, 10),
    (datetime.fromisoformat("2022-03-14T12:20:00+01:00").replace(tzinfo=timezone.utc), 23.9, 1013.3, 0.6, 15),
    (datetime.fromisoformat("2022-03-14T12:30:00+01:00").replace(tzinfo=timezone.utc), 24.1, 1013.5, 0.58, 20),
    (datetime.fromisoformat("2022-03-14T12:40:00+01:00").replace(tzinfo=timezone.utc), 24.2, 1013.6, 0.56, 25),
]

# Convert data to numpy array for easier processing
data = np.array(data)

# Split data into X (inputs) and y (output)
X = data[:, 1:4].astype(float)
y = data[:, 4].astype(float)

# Create linear regression model and train it on the initial data
regressor = LinearRegression()
regressor.fit(X, y)

# Set up a loop to generate new data every 5 minutes and predict the temperature in 10 minutes
while True:
    # Get current time and round up to the nearest 5 minutes
    now = datetime.now(timezone.utc)
    next_time = now + timedelta(minutes=5)
    next_time = next_time - timedelta(minutes=next_time.minute % 5, seconds=next_time.second, microseconds=next_time.microsecond)
    
    # Wait until next_time
    time_diff = (next_time - now).total_seconds()
    if time_diff > 0:
        wait_loop(time_diff)
    
    # Generate new data point
    current_temp = np.random.normal(25, 2)
    current_pressure = np.random.normal(1015, 5)
    current_humidity = np.random.normal(0.5, 0.1)
    current_wind = np.random.normal(10, 5)
    new_data = np.array([[current_temp, current_pressure, current_humidity, current_wind]])
    
    # Predict temperature in 10 minutes using the new data
    future_pressure = new_data[0][1]
    future_humidity = new_data[0][2]
    future_wind = new_data[0][3]
    future_X = np.array([[current_temp, future_pressure, future_humidity, future_wind]])
    future_temp = regressor.predict(future_X)[0]

    # Print current and predicted temperature
    print(f"Current temperature: {current_temp:.1f} °C")
    print(f"Predicted temperature in 10 minutes: {future_temp:.1f} °C\n")

    """
    This code is just for testing purposes. It is not part of the actual bot.
    import json

    import requests
    import urllib.parse
    from unix_to_realtime import unix_to_realtime
    
    
    class WeatherSystem:
    
        def __init__(self, name: str):
            self.name = name
            self.api_key = "e82189d6bac853490363d9691e94e013"
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
"""