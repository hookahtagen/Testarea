import requests


def get_air_pressure(lat, lon, api_key):
    """
    Function to get the air pressure for a given latitude and longitude using the OpenWeather API.

    Args:
        lat (float): The latitude of the location.
        lon (float): The longitude of the location.
        api_key (str): Your OpenWeather API key.

    Returns:
        float: The air pressure in hPa.
    """
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        air_pressure = data['main']['pressure']
        return air_pressure
    else:
        return None

def calculate_relative_height(measured_pressure):
    """
    Calculates the relative height based on sea level pressure and measured pressure.

    Args:
        sea_level_pressure (float): Sea level pressure in pascals.
        measured_pressure (float): Measured pressure from the BMP280 sensor in pascals.

    Returns:
        float: The calculated relative height in meters.
    """
    sea_level_pressure = 1013.25
    temperature = 15.39  # Replace with actual temperature in Celsius

    temperature_k = temperature + 273.15
    lapse_rate = 0.0065

    relative_height = ((sea_level_pressure/measured_pressure)
                       ** (1/5.257) - 1) * (temperature_k) / lapse_rate

    return relative_height


if __name__ == '__main__':
    mode = "h"

    if mode == "h":
        local_pressure = 1007.19
        
        relative_height = calculate_relative_height(local_pressure)
        
        print(f"Relative height: {relative_height}")
    elif mode == "p":
        api_key = '8ada6ef1f544553120e0a962d9e07dbb'
        lat = 52.516181
        lon = 13.376935

        air_pressure = get_air_pressure(lat, lon, api_key)

        print(f'The air pressure is {air_pressure} hPa.')
