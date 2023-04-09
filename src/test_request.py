from typing import Union

import requests


def get_outside_params() -> Union[dict, None]:

        api_key = "087d43f5068c9c22dad4af4e8e47bc63"
        latitude = 51.7396472
        longitude = 8.2510176

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return {
                "temperature": data["main"]["temp"],
                "air_pressure": data["main"]["pressure"],
                "humidity": data["main"]["humidity"]
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
        

data = get_outside_params()

print(data)