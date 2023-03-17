"""
This program uses a BMP280 sensor to measure temperature and pressure and a DHT22 sensor to measure humidity.
The data is then logged to a database for further processing.
"""

import time
from typing import Optional

import board
import adafruit_dht
import adafruit_bmp280

import sqlite3
import socket


# noinspection PyUnboundLocalVariable
def connect_to_database(server: str, database_name: str, flag: Optional[int] = 1, db_file: str = ""):
    """
    Stellt eine Verbindung zu einer SQLite-Datenbank auf einem anderen Server her.

    :param db_file:
    :param flag: 1 for local database, 0 for remote database
    :param server: Name or Ip address of the server.
    :param database_name: Name of the database.
    :return: Connection to the database or None if the connection could not be established.
    """
    
    if flag == 1:
        db_file = server + "/" + database_name

    elif flag == 0:
        # Versucht den Hostnamen in eine IP-Adresse aufzulösen
        try:
            server_ip = socket.gethostbyname(server)
        except socket.gaierror as e:
            print(f"Hostname could not be resolved: {e}")
            return None

        # Verbindung zur SQLite-Datenbank herstellen
    try:
        if flag == 1:
            con = sqlite3.connect(db_file)
        elif flag == 0:
            con = sqlite3.connect(f"file:/\\/{server_ip}/{database_name}?mode=rw", uri=True)
        return con
    except sqlite3.Error as e:
        print(f"Error ecountered while connecting to the database: {e}")
        return None


def set_datapoint(con, data) -> bool:
    """
    - Description: \n
    Saves a datapoint to the database.
    Each datapoint consists of a timestamp, temperature, pressure and humidity.
    It will be saved to the table "weather_data".

    - Structure of the table:\n
    | id | timestamp | temperature | pressure | humidity |


    - Explanation of the columns:\n
    id - integer - primary key - autoincrement - not null
    timestamp - real - not null
    temperature - real - not null
    pressure - real - not null
    humidity - real - not null

    :param con: Connection to the database.
    :param data: Tuple containing the timestamp, temperature, pressure and humidity.
    :return: bool: True if the data was successfully saved to the database.
    """
    time_stamp, temperature, pressure, humidity = data
    values = (time_stamp, temperature, pressure, humidity)
    sql_query = "INSERT INTO weather_data (timestamp, temperature, pressure, humidity) VALUES (?, ?, ?, ?)"

    try:
        # Insert the data into the database
        cursor = con.cursor()
        cursor.execute(sql_query, values)
        con.commit()
        ack = True
    except sqlite3.Error as e:
        print(f"Error encountered while saving data to the database: {e}")
        ack = False

    return ack


def run(con: sqlite3.connect):
    # Datenbankverbindung prüfen
    if con is None:
        print("Connection could not be established.")
        exit(1)

    dht = adafruit_dht.DHT22(board.D4)
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(board.I2C())

    while True:
        try:
            # Messwerte der Sensoren auslesen
            time_stamp = time.time()
            temperature = bmp280.temperature
            pressure = bmp280.pressure
            humidity = dht.humidity

            # Messwerte ausgeben
            print("Timestamp: {:.2f}".format(time_stamp))
            print("Temperature: {:.2f}°C".format(temperature))
            print("Air pressure: {:.2f}hPa".format(pressure))
            print("Relative humidity: {:.2f}%".format(humidity))

            set_datapoint(con, (time_stamp, temperature, pressure, humidity))

        except RuntimeError as e:
            # Fehlerbehandlung, falls es zu Problemen bei der Messung kommt
            print("Error while taking measurements:", e.args[0])

        # 5 Minuten warten
        time.sleep(300)


def main():
    # Verbindung zur Datenbank herstellen
    con = connect_to_database("192.168.2.17", "weather.db", 0)
    run(con)


if __name__ == '__main__':
    conn = connect_to_database("/home/hendrik/Documents/Github/Testarea/data/", "weather.db", 1)
    if conn:
        print("Successfully connected to the database.")
        ret = True
    else:
        print("Connection could not be established.")
        ret = False

    exit(0 if ret else 1)
