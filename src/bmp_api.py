"""
This program is a simpler API to the BMP280 sensor.
It is used to read the data from the sensor and return the values.

"""
import datetime
import subprocess
from flask import Flask, request, jsonify


app = Flask(__name__)


def read_bmp280():
    bmp280_addr = 0x76
    temperature_offset = 0.0

    command = f"read_bme280 --i2c-address {bmp280_addr}"
    data = subprocess.check_output(command.split())
    data = data.decode("utf-8").split("\n")

    temperature: str = data[2]
    pressure: str = data[0]
    humidity: str = data[1]

    return temperature, pressure, humidity


@app.route("/environment-data", methods=["GET"])
def environment_data():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    temperature, pressure, humidity = read_bmp280()
    return jsonify({
	"Time": current_time,
        "temperature": temperature,
        "pressure": pressure,
        "humidity": humidity
    })


if __name__ == "__main__":
    app.run(host="192.168.2.55", port=6000, debug=True)
    
