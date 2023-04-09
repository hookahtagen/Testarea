import math
import sys
import threading
import time
from typing import Union
import RPi.GPIO as GPIO
import smbus2
from hc_sr04 import clear_screen
import requests
import bme280

from threading import Thread

from test_buzzer import set_emergency_stop, buzz, beep_n_times


class DEFINE:
    RELAY_ENABLE = True
    RELAY_LIST = [13, 19, 26]
    RELAY_1 = 13
    RELAY_2 = 19
    RELAY_3 = 26


class heater_system:
    def __init__(self, name) -> None:
        self.name = name
        self.in_temperature = 0.0
        self.pressure = 0.0
        self.humidity = 0.0

        self.heat_flow_glass = 0.0
        self.heat_flow_wood_wall = 0.0
        self.heat_flow_roof = 0.0
        self.dew_point_temperature = 0.0

        self.heating_level = [0, 0, 0]

        self.i2c_address = 0x76
        self.i2c_bus_1 = smbus2.SMBus(1)
        self.i2c_bus_3 = smbus2.SMBus(3)

        self.calibration_params_1 = bme280.load_calibration_params(
            self.i2c_bus_1, self.i2c_address)
        self.calibration_params_3 = bme280.load_calibration_params(
            self.i2c_bus_3, self.i2c_address)

        self.is_running = False
        self.machine = Thread(target=self.machine_thread, daemon=True)
        self.heating_control_thread = Thread(
            target=self.heating_control, daemon=True)
        self.timer = threading.Timer(300.0, self.turn_off_power)

        self.get_initial_state()

    def turn_off_power(self):
        beep_n_times(6)
        for relay in DEFINE.RELAY_LIST:
            GPIO.output(relay, GPIO.LOW)

    def get_initial_state(self):
        self.read_bme280(3)

    def calc_params(self):

        u_value_glass = 5.706
        u_value_wood_wall = 2.588
        u_value_roof = 2.404
        area_floor = 9
        area_door_window = 0.541 * 0.738
        area_front_window = 0.693 * 0.912
        area_double_window = 1.298 * 0.912
        area_glass = area_door_window * area_front_window * area_double_window
        area_wood_wall = 4 * (3 * 1.938) - area_glass
        area_roof = 1.572 * 3.2

        outside_temperature = self.read_bme280(1)

        self.heat_flow_glass = u_value_glass * area_glass * \
            (self.in_temperature - outside_temperature)
        self.heat_flow_wood_wall = u_value_wood_wall * area_wood_wall * \
            (self.in_temperature - outside_temperature)
        self.heat_flow_roof = u_value_roof * area_roof * \
            (self.in_temperature - outside_temperature)

        self.total_heat_flow = self.heat_flow_glass + \
            self.heat_flow_roof + self.heat_flow_wood_wall

        if self.humidity == 0.0:
            self.humidity = 0.1

        # Temperatur über 0 ° C: k2=17.62, k3=243.12
        #
        # Temperatur 0 ° C oder darunter: k2=22.46, k3=272.62
        #
        # Temperatur t, Luftfeuchtigkeit l
        #
        # Taupunkt = k3*( ( k2 * t ) / ( k3 + t ) + ln( l / 100 ) ) / ( ( k2 * k3 )/ ( k3 + t ) - ln( l / 100 ) )

        if self.in_temperature > 0:
            k2 = 17.62
            k3 = 243.12
        if self.in_temperature <= 0:
            k2 = 22.46
            k3 = 272.62

        coefficient_1 = math.log(self.humidity / 100)
        self.dew_point_temperature = k3*((k2 * self.in_temperature) / (
            k3 + self.in_temperature) + coefficient_1) / ((k2 * k3) / (k3 + self.in_temperature) - coefficient_1)

    def get_outside_params(self) -> Union[dict, None]:

        api_key = "087d43f5068c9c22dad4af4e8e47bc63"
        latitude = 51.7396472
        longitude = 8.2510176

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            print(data["main"]["temp"])
            return {
                "temperature": data["main"]["temp"],
                "air_pressure": data["main"]["pressure"],
                "humidity": data["main"]["humidity"]
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def console_timer(self, seconds: int, msg: str) -> None:
        for i in range(0, seconds):
            clear_screen()
            print(msg)
            print(f"Remaining seconds till next data: {seconds - i}")
            time.sleep(1)

    def heating_control(self):
        global timer

        GPIO.setmode(GPIO.BCM)

        heating_level = [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [1, 0, 0]
        ]
        while self.is_running:
            if self.heating_level == heating_level[0]:
                for relay in DEFINE.RELAY_LIST:
                    GPIO.output(relay, GPIO.LOW)

                beep_n_times(5)
            elif self.heating_level == heating_level[1]:
                # heating level 1: 1000 W
                GPIO.output(DEFINE.RELAY_1, GPIO.HIGH)
                GPIO.output(DEFINE.RELAY_2, GPIO.LOW)
                GPIO.output(DEFINE.RELAY_3, GPIO.LOW)
                beep_n_times(1)
            elif self.heating_level == heating_level[2]:
                # heating level 2: 1500 W
                GPIO.output(DEFINE.RELAY_1, GPIO.LOW)
                GPIO.output(DEFINE.RELAY_2, GPIO.HIGH)
                GPIO.output(DEFINE.RELAY_3, GPIO.LOW)
                beep_n_times(2)
            elif self.heating_level == heating_level[3]:
                # heating level 3: 2300 W
                GPIO.output(DEFINE.RELAY_1, GPIO.LOW)
                GPIO.output(DEFINE.RELAY_2, GPIO.LOW)
                GPIO.output(DEFINE.RELAY_3, GPIO.HIGH)
                beep_n_times(3)
            else:
                print("ELSE")
                if self.in_temperature <= 5:
                    # In case the temperature is below or is equal to 5 degrees
                    # maximum power is selected for safety purposes (frost prevention, etc.)
                    GPIO.output(DEFINE.RELAY_1, GPIO.LOW)
                    GPIO.output(DEFINE.RELAY_2, GPIO.LOW)
                    GPIO.output(DEFINE.RELAY_3, GPIO.HIGH)
                else:
                    for relay in DEFINE.RELAY_LIST:
                        GPIO.output(relay, GPIO.LOW)

                beep_n_times(5)

            time.sleep(1)

        # In case the thread is stopped, power to the
        # heating elements is cutoff.
        for relay in DEFINE.RELAY_LIST:
            GPIO.output(relay, GPIO.LOW)

    def machine_thread(self):
        i = 0
        while self.is_running:
            global clear_screen

            clear_screen()
            self.read_bme280(3)
            self.calc_params()

            if self.total_heat_flow <= 1000:
                self.heating_level = [0, 0, 1]
            elif 1000 < self.total_heat_flow <= 1500:
                self.heating_level = [0, 1, 0]
            else:
                self.heating_level = [1, 0, 0]

            env_data_msg = f"""
            Temperature\t{self.in_temperature} °C
            Pressure\t{self.pressure} hPa
            Humidity:\t{self.humidity} %
            
            Dew point temperature {self.dew_point_temperature} °C
            Heat flow glass: {self.heat_flow_glass} W
            Heat flow wood wall: {self.heat_flow_wood_wall} W
            Heat floe roof: {self.heat_flow_roof} W
            """
            print(env_data_msg)
            self.console_timer(15, env_data_msg)
        print("Stopping the system")

    def start(self):
        self.is_running = True
        self.machine.start()
        self.heating_control_thread.start()

    def stop(self):
        exit_msg = """
        Stop button pressed.
        Exiting now...

        And yes, that's a error message below. You might wanna ignore it.
        Or you can dig deeper down the rabbit hole. I'm fine for now.
        """
        print(exit_msg)
        self.is_running = False

    def read_bme280(self, bus: int) -> Union[int, None]:
        if bus == 1:
            data = bme280.sample(
                self.i2c_bus_1, self.i2c_address, self.calibration_params_1)

            return data.temperature

        if bus == 3:
            data = bme280.sample(
                self.i2c_bus_3, self.i2c_address, self.calibration_params_1)

            self.in_temperature = data.temperature
            self.pressure = data.pressure
            self.humidity = data.humidity


def relay_enable():
    pass


def setup():
    GPIO.setmode(GPIO.BCM)

    clear_screen()
    heater = heater_system("heater1")
    relay_enable_thread = Thread(target=relay_enable, daemon=True)
    relay_enable_thread.start()

    relay_card_connect_channel = 10

    set_emergency_stop(21, True)
    set_emergency_stop(relay_card_connect_channel, False)

    for relay in DEFINE.RELAY_LIST:
        GPIO.setup(relay, GPIO.OUT)
        GPIO.output(relay, GPIO.LOW)

    if GPIO.input(relay_card_connect_channel) == 0:
        print("Relay card not connected!")
        sys.exit(0)
    elif GPIO.input(relay_card_connect_channel) == 1:
        print("Relay card connected\n\n")
        time.sleep(1)

    return heater


def main(heater: heater_system) -> bool:
    ret = True

    heater.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        del heater

    return ret


if __name__ == '__main__':
    global heater

    heater = setup()
    ack = main(heater)

    GPIO.cleanup()
    exit(0 if ack else 1)
