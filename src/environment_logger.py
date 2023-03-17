import sqlite3
import time
import requests


def read_sensor() -> tuple[str, str, str]:
    api_url = "http://192.168.2.55:5000/environment_data"
    response = requests.get(api_url)

    # Remove any characters after the first whitespace
    temperature = response.json()["temperature"].split()[0]
    pressure = response.json()["pressure"].split()[0]
    humidity = response.json()["humidity"].split()[0]

    return temperature, pressure, humidity


def run_sensor_test() -> bool:
    temperature, pressure, humidity = read_sensor()
    print(f"Temperature: {temperature} °C")
    print(f"Pressure: {pressure} hPa")
    print(f"Humidity: {humidity} %")

    return True


def db_connect(database: str) -> sqlite3.connect:
    try:
        con = sqlite3.connect(database)
        print("Connection to database established.")
    except sqlite3.Error as e:
        print(f"Error encountered while connecting to the database: {e}")
        con = None

    return con


def main():
    database = "../data/environment.db"

    conn = db_connect(database)
    if conn is None:
        print("Database connection could not be established.")
        return False

    print("Measurement finished.")
    print("You can find the measurement data in the file \"environment.log\".")
    print("Goodbye.")
    return True


if __name__ == '__main__':
    print("Starting measurement...")
    print("This will take about 24 hours.")
    print("Please wait...")

    exit(0 if main() else 1)
