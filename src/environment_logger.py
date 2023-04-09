import sqlite3
import time
import requests


# noinspection PyPep8Naming
class constants:
    UPDATE_INTERVAL = 5


def read_sensor() -> tuple[str, str, str]:
    api_url = "http://192.168.2.55:6000/environment-data"
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


def update_data_point(con: sqlite3.connect, data: tuple) -> bool:
    ack = False
    time_stamp, temperature, pressure, humidity = data
    values = (time_stamp, temperature, pressure, humidity)
    sql_query = "INSERT INTO environment_data (timestamp, temperature, pressure, humidity) VALUES (?, ?, ?, ?)"

    try:
        # Insert the data into the database
        cursor = con.cursor()
        cursor.execute(sql_query, values)
        con.commit()
        ack = True
    except sqlite3.Error as e:
        print(f"Error encountered while saving data to the database: {e}")
        ack = False
    finally:
        if ack is False:
            con.rollback()
        elif ack is True:
            print("Data point saved to database.")

    return ack


def main():
    database = "/home/hendrik/Projects/Testarea/data/weather.db"

    conn = db_connect(database)
    if conn is None:
        return False

    run_sensor_test()  # Test if the sensor is working and connected to the network

    run_time = 86400  # 24 hours
    while run_time > 0:
        data = read_sensor()
        time_stamp = time.time()
        update_data_point(conn, (time_stamp, data[0], data[1], data[2]))

        time.sleep(constants.UPDATE_INTERVAL)
        run_time -= constants.UPDATE_INTERVAL

    print("Measurement finished.")
    print("You can find the measurement data in the file \"environment.log\".")
    print("Goodbye.")
    return True


if __name__ == '__main__':
    time.sleep(4)
    print("Starting measurement...")
    print("This will take about 24 hours.")
    print("Please wait...")

    exit(0 if main() else 1)
