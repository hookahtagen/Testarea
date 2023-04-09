import math
import os
from socket import send_fds
import sys
import threading
from typing import Union
import RPi.GPIO as GPIO
import time
import subprocess
import sqlite3

GPIO.setwarnings(False)

def clear_screen():
    # Clear the screen depending on the OS (MacOS, Linux, Windows)
    os.system("clear") if sys.platform == "linux" else os.system("cls")


class Database:
    def __init__(self, name: str, db_path: str) -> None:
        self.name = name
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)

        self.data = []

    def db_query(self, query: str, data: list[float, float, float], fetch=None) -> Union[list, bool]:
        sql_query = query
        values = data
        cursor = self.conn.cursor()
        cursor.execute(sql_query, values)

        if fetch != None:
            result = []
            if fetch == "all":
                result = cursor.fetchall()
            elif fetch == "one":
                # fetch one and store it in a list
                result = [cursor.fetchone()]

            return result
        else:
            cursor.execute(sql_query, values)
            self.conn.commit()

            result = self.db_query("SELECT (?, ?, ?)", data, "all")
            if result == []:
                return False
            else:
                return True

    def db_close(self):
        self.conn.close()

        return True if not self.conn else False


class DistanceSensor:
    def __init__(self, name: str, triggerpin: int, echopin: int) -> None:
        self.trigger_pin = triggerpin
        self.echo_pin = echopin

        self.speed_of_sound = 0.0
        self.last_bme280_read = 0.0

        self.start_time = None

        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def compensate_temperatur(self) -> int:
        speed_of_sound: float = 0.0

        self.last_bme280_read = time.time()
        output = subprocess.check_output(
            ["/home/hendrik/.local/bin/read_bme280"]).decode("utf-8")
        temperature = float(output.split("\n")[2].split()[0])

        speed_of_sound = 331.3 * math.sqrt(1 + (temperature / 273.15))
        speed_of_sound = speed_of_sound * 100  # convert m/s to cm/s

        return speed_of_sound

    def wait_for_echo(self):
        start_time = time.time()
        end_time = time.time()
        
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()
        while GPIO.input(self.echo_pin) == 1:
            end_time = time.time()

        time_elapsed = end_time - start_time
        return time_elapsed

    def send_pulse(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.000001)
        GPIO.output(self.trigger_pin, False)

    def measure_distance(self):#
        self.send_pulse()
        time_elapsed = self.wait_for_echo()

        if time.time() - self.last_bme280_read > 15:
            # Compensate the effect of temperature on the speed of sound
            self.speed_of_sound = self.compensate_temperatur()
        distance = (time_elapsed * self.speed_of_sound) / 2

        if distance < 2 or distance > 390:
            return -1

        return distance

    def measure_and_print_distance(self):
        try:
            while True:
                dist = self.measure_distance()
                if dist != -1:
                    print("Measured distance = %.1f cm" % dist)
                    time.sleep(2)
                else:
                    print("Out of range")
                    time.sleep(2)

        except KeyboardInterrupt:
            print("Measurement stopped by User")


class StepperMotor:
    def __init__(self, name: str, pinlist: list[int, int, int, int], speed: float) -> None:
        self.name = name
        self.pin = pinlist
        self.step_sleep = speed  # 2ms
        # 5.625*(1/64) per step, 4096 steps is 360°  2*8192 = 16  2*16384 = 32
        self.step_count = 4096
        self.direction = False  # True for clockwise, False for counter-clockwise
        self.step_sequence = [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]]
        for i in range(0, 4):
            GPIO.setup(self.pin[i], GPIO.OUT)
            GPIO.output(self.pin[i], GPIO.LOW)

        self.motor_pins = [self.pin[0], self.pin[1], self.pin[2], self.pin[3]]
        self.motor_step_counter = 0

    def cleanup(self):
        GPIO.cleanup()

    def full_turn(self, mode: str):
        self.direction = mode
        try:
            self.motor_step_counter = 0
            i = 0
            for i in range(self.step_count):

                for pin in range(0, len(self.motor_pins)):
                    GPIO.output(
                        self.motor_pins[pin], self.step_sequence[self.motor_step_counter][pin])

                if self.direction == True:
                    motor_step_counter = (motor_step_counter - 1) % 8

                elif self.direction == False:
                    motor_step_counter = (motor_step_counter + 1) % 8

                else:  # defensive programming
                    print("uh oh... direction should *always* be either True or False")
                    self.cleanup()
                    sys.exit(1)

                time.sleep(self.step_sleep)

        except KeyboardInterrupt:
            pass

    def turn_by_degree(self, mode: str, degree: float) -> None:
        self.direction = mode
        one_degree: float = self.step_count / 360
        turn_rate: int = int(degree * one_degree)

        try:
            self.motor_step_counter = 0
            i = 0
            for i in range(turn_rate):

                for pin in range(0, len(self.motor_pins)):
                    GPIO.output(
                        self.motor_pins[pin], self.step_sequence[self.motor_step_counter][pin])

                if self.direction == True:
                    self.motor_step_counter = (self.motor_step_counter - 1) % 8

                elif self.direction == False:
                    self.motor_step_counter = (self.motor_step_counter + 1) % 8

                else:  # defensive programming
                    print("uh oh... direction should *always* be either True or False")
                    self.cleanup()

                time.sleep(self.step_sleep)

        except KeyboardInterrupt:
            pass


def test_setup(pinlist: list[int, int, int, int], sensor: DistanceSensor) -> None:
    motor = StepperMotor(
        name="mot1",
        pinlist=pinlist,
        speed=0.002
    )
    try:
        while GPIO.input(10) == GPIO.HIGH:
            dist_list = []
            sample_size = 1
            for _ in range(sample_size):
                dist_list.append(sensor.measure_distance())
                # time.sleep(0.01)
            dist = sum(dist_list) / len(dist_list)

            clear_screen()
            print("Out of range\n-") if dist == -1 else None

            if dist != -1:
                print(f"Measured distance = {dist:.1f} cm\n-")
                if dist < 10:
                    motor.turn_by_degree(mode=False, degree=5)
                    # If the distance is high enough,
                    # all pins in the pinlist will be set to low
            conditions = [
                dist > 10,
                dist == -1]
            if any(conditions):
                for pin in pinlist:
                    GPIO.output(pin, GPIO.LOW)

            time.sleep(1)

        if GPIO.input(10) == GPIO.LOW:
            print("Relay card disconnected!")
            print("Reconnect the relay card and restart the program.")

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


def read_keypad(ROW_PINS, COL_PINS):
    KEY_MAP = {
        (0, 0): '1',
        (0, 1): '2',
        (0, 2): '3',
        (0, 3): 'A',
        (1, 0): '4',
        (1, 1): '5',
        (1, 2): '6',
        (1, 3): 'B',
        (2, 0): '7',
        (2, 1): '8',
        (2, 2): '9',
        (2, 3): 'C',
        (3, 0): '*',
        (3, 1): '0',
        (3, 2): '#',
        (3, 3): 'D'}

    # Initialize the keys list to all None
    keys = [[None, None, None, None], [None, None, None, None],
            [None, None, None, None], [None, None, None, None]]
    # Loop through each row pin and column pin
    for row_num, row_pin in enumerate(ROW_PINS):
        for col_num, col_pin in enumerate(COL_PINS):
            # Set the current column pin to high
            GPIO.output(col_pin, GPIO.HIGH)
            # Read the state of the current row pin
            if GPIO.input(row_pin):
                # Update the keys list with the pressed key label
                keys[row_num][col_num] = KEY_MAP[(row_num, col_num)]
            # Set the current column pin back to low
            GPIO.output(col_pin, GPIO.LOW)
    # Return the keys list
    return keys


def read_motor_speed(RowPins, ColPins):
    speed = ''
    flag = False
    # Read the motor speed from the keypad - exit when the user hits the * key
    while not flag:
        # Read the state of the keypad
        keys = read_keypad(RowPins, ColPins)
        # Loop through each row in the keys list
        for row_num, row in enumerate(keys):
            # Loop through each key in the current row
            for col_num, key in enumerate(row):
                # Check if the current key has been pressed
                if key is not None:
                    # Check if the current key is the * key
                    conditions = ['*', 'A', 'B', 'C', 'D']
                    if key in conditions:
                        # Exit the loop
                        # Check if the key is a letter or a asterisk
                        if key in conditions[1:]:
                            # Set the speed to the corresponding value
                            speed = {
                                'A': '0.002',
                                'B': '0.004',
                                'C': '0.006',
                                'D': '0.008'
                            }[key]
                        if key == '*':
                            # Set the speed
                            # If a # is present in the speed string, replace it with a .
                            speed = float(speed.replace('#', '.'))

                        flag = True
                        return speed
                    # Otherwise, add the key to the speed string

                    speed += key
        # Wait 100ms before re-reading the keypad
        time.sleep(0.15)

def stop_at_button(channel):
    print("Exiting now...")
    GPIO.cleanup()
    sys.exit(0)

def setup():
    """Setup the GPIO pins"""
    GPIO.setmode(GPIO.BCM)

    ROW_PINS = [14, 15, 18, 23]
    COL_PINS = [24, 25, 8, 7]
    dist_sense_pinlist = [20, 21]
    motor_pinlist = [6, 13, 19, 26]
    relay_channels = [0, 0, 0, 0, 0, 0]
    
    interrupt_channel = 9

    out_channels = [20]
    speed = 0.002
    
    GPIO.setup(interrupt_channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(interrupt_channel, GPIO.RISING, callback=stop_at_button, bouncetime = 100)

    # row pins and pin 10
    for pin in ROW_PINS + [10]:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    for pin in COL_PINS:
        GPIO.setup(pin, GPIO.OUT)
        
    for channel in out_channels:
                GPIO.setup(channel, GPIO.OUT)
                GPIO.output(channel, GPIO.LOW)
                
    if GPIO.input(10) == GPIO.HIGH:
        print("Relay card detected\n")
        time.sleep(2)

        print(f"Please specify the motor speed (0.002 - 0.01).")
        print(f"Or use one of the presets on buttons A - D")
        print(f"Use the # key as a decimal point.")
        print(f"Press * to set the speed.")
        speed: float = read_motor_speed(ROW_PINS, COL_PINS)

        print(f"Selected speed: {speed}")
        print(f"Please hit Enter to continue or CTRL + C to exit and start again")
        print(f"If you don't press any button, the program will start in 10 seconds")
        
        input()

    else:
        print(f"No relay card detected")
        print(f"Please make sure the relay card is connected to the Pi")
        print(f"Exiting...")

        GPIO.cleanup()
        sys.exit(1)

    return motor_pinlist, dist_sense_pinlist, relay_channels, speed


if __name__ == "__main__":
    clear_screen()
    motor_pinlist, dist_sense_pinlist, relay_channels, speed = setup()

    print("Starting...")
    print("Test")
    sensor = DistanceSensor(
        "DistanceSensor",
        triggerpin=dist_sense_pinlist[0],  # dist_sense_pinlist 0
        echopin=dist_sense_pinlist[1])  # dist_sense_pinlist 1
    test_setup(motor_pinlist, sensor)

    print("Exiting...")
    GPIO.cleanup()
