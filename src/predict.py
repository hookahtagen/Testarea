import sqlite3

import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timezone, timedelta


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
        temp, pressure, humidity, wind = data[i][1], data[i][2], data[i][3], data[i][4]
        next_temp = data[i+1][1]
        X.append([temp, pressure, humidity, wind])
        y.append(next_temp)

    # Das letzte Element der Daten als Input-Vektor für die Vorhersage nutzen
    last_temp, last_pressure, last_humidity, last_wind = data[-1][1], data[-1][2], data[-1][3], data[-1][4]
    future_pressure, future_humidity, future_wind = last_pressure, last_humidity, last_wind
    future_time = data[-1][0] + timedelta(minutes=10)

    # Eine lineare Regression auf den Daten durchführen
    regressor = LinearRegression()
    regressor.fit(X, y)

    # Die Temperatur in 10 Minuten vorhersagen
    future_X = np.array([[last_temp, future_pressure, future_humidity, future_wind]])
    future_temp = regressor.predict(future_X)[0]

    # Die Vorhersage ausgeben
    return future_time, future_temp


if __name__ == '__main__':
    database = "../data/weather.db"
    conn = db_connect(database)

    data_interval = 5 * 60  # 5 Minuten
    prediction_interval = 10 * 60  # 10 Minuten

    # Load the data of the last 5 minutes from the database
    cursor = conn.cursor()
    sql_query = f"SELECT * FROM environment_data WHERE timestamp > {int(datetime.now().timestamp()) - data_interval}"
    cursor.execute(sql_query)
    data = cursor.fetchall()

    # Predict the temperature in 10 minutes
    future_time, future_temp = predict_temperature(data)

    print(f"Temperature at {future_time}: {future_temp} °C")
