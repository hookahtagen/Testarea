import sqlite3
import time

import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta


def db_connect(database: str) -> sqlite3.Connection | None:
    """
    This function creates a connection to the SQLite database.
    :param database: str
    :return: sqlite3.Connection
    """
    con = None

    try:
        con = sqlite3.connect(database)
    except sqlite3.Error as e:
        print(e)

    if con:
        print("Connection to database established.")
        return con
    else:
        print("Connection to database could not be established.")
        return None


# noinspection PyShadowingNames
def predict_temperature(data):
    # Aus den Daten die Input- und Output-Variablen für die lineare Regression erstellen
    X = []
    y = []
    for i in range(len(data)-1):
        temp, pressure, humidity,  = data[i][1], data[i][2], data[i][3]
        next_temp = data[i+1][1]
        X.append([temp, pressure, humidity])
        y.append(next_temp)

    # Das letzte Element der Daten als Input-Vektor für die Vorhersage nutzen
    last_temp, last_pressure, last_humidity = data[-1][1], data[-1][2], data[-1][3]
    future_pressure, future_humidity = last_pressure, last_humidity
    future_time = data[-1][0] + 10 * 60

    # Eine lineare Regression auf den Daten durchführen
    regressor = LinearRegression()
    regressor.fit(X, y)

    # Die Temperatur in 10 Minuten vorhersagen
    future_x = np.array([[last_temp, future_pressure, future_humidity]])
    future_temp = regressor.predict(future_x)[0]

    # Die Vorhersage ausgeben
    return future_time, future_temp


if __name__ == '__main__':
    conn = sqlite3.connect('../data/weather.db')
    c = conn.cursor()

    # Get the current time in UTC timezone
    now = time.time()
    five_minutes_ago = now - 5 * 60

    query = f"SELECT timestamp, temperature, pressure, humidity FROM environment_data WHERE timestamp > {five_minutes_ago}"
    data = c.execute(query).fetchall()

    # Predict the temperature in 10 minutes
    future_time, future_temp = predict_temperature(data)

    real_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(future_time))
    print(f"Temperature at {real_time}: {future_temp} °C")
