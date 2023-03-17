# For later use:
# import math
import subprocess
import threading
import time

from threading import Thread


def clear_screen():
    subprocess.call("clear")


# noinspection PyPep8Naming
class constants:
    POST_ADDR1 = "Bluddenstraße 5, Wadersloh, Germany"
    CHECK_INTERVAL = 15
    NOTIFY_INTERVAL = 20
    THERMAL_TRANSMITTANCE_COEFFICIENT = 0.5
    AREA = 1.0
    ROOM_VOLUME = 1.0
    M_SATURATION = 0.5
    B = 17.27
    C = 237.7
    BMP280_ADDR = 0x76
    TEMPERATURE_OFFSET = 0.0


class GpioInterface:
    def __init__(self, name: str):
        self.name = name
        current_time = time.time()
        self.parameters = {
            f"{current_time}": (None, None, None)
        }
        self.update_parameter_readings()

    def update_parameter_readings(self):
        temperature, pressure, humidity = self.read_bmp280()

        self.parameters = {  # Update the parameters
            f"{time.time()}": (temperature, pressure, humidity)
        }

    @staticmethod
    def read_bmp280():
        import subprocess
        command = "read_bme280 --i2c-address 0x76"
        data = subprocess.check_output(command.split())
        data = data.decode("utf-8").split("\n")

        temperature: str = data[2]
        pressure: str = data[0]
        humidity: str = data[1]

        return temperature, pressure, humidity


# noinspection PyAttributeOutsideInit
class ClimateLink:
    def __init__(self, name: str = "ClimateLink", sensor: GpioInterface = None, time_interval: int = 15):
        self.name = name
        self.interval = time_interval
        self.sensor = sensor
        self.param_lock = threading.Lock()
        self.parameters = self.sensor.parameters

        # Start a thread
        # The thread will run the method "update_parameter_readings" every 5 minutes
        # and update the parameters of the "ClimateLink" object

        self.is_running = False
        self.enviroment_logger = Thread(target=self.update_parameters, daemon=True)

    def update_parameters(self):
        while self.is_running:
            self.sensor.update_parameter_readings()
            self.parameters = self.sensor.parameters
            time.sleep(self.interval)
        print("Measurement thread stopped.")

    def start(self):
        self.is_running = True
        print("Measuring will start soon...")
        print("Full measurement cycle will take 5 minutes.")
        print("Please wait...")
        print("You can stop the measurement by pressing CTRL+C.")
        self.enviroment_logger.start()

    def stop(self):
        self.is_running = False
        self.enviroment_logger.join()


def main():
    log_file = "./environment.log"
    # Initialize the GPIO interface
    gpio = GpioInterface(name="GPIO")
    cl = ClimateLink(sensor=gpio, time_interval=1)
    cl.start()

    notify_str = """
    ******************************
    *                            *
    *   ClimateLink is running   *
    *                            * 
    ******************************
    """
    print(notify_str)

    # Get the latest data from the sensor
    latest_time = max(cl.parameters.keys())
    latest_data = cl.parameters[latest_time]
    print("Latest data:")
    print(f"Temperature: {latest_data[0]}")
    print(f"Pressure: {latest_data[1]}")
    print(f"Humidity: {latest_data[2]}")

    time.sleep(5)
    clear_screen()

    print(notify_str)

    try:
        measurement_time = 86400
        with open(log_file, "w") as logfile:
            while measurement_time >= 0:
                logfile.write(str(cl.parameters) + "\n")
                time.sleep(constants.CHECK_INTERVAL)
                measurement_time -= 1
        ret = True
    except Exception as e:
        print("Something went wrong while measuring the environment data.")
        print(e)

        ret = False
    finally:
        cl.stop()
        print("Measurement stopped.")
        print("You can find the measurement data in the file \"environment.log\".")
        print("Goodbye.")

    return ret


if __name__ == '__main__':
    exit(0 if main() else 1)
