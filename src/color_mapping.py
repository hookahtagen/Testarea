import time
import RPi.GPIO as GPIO
from gpiozero import MCP3008


def clear_screen():
    print('\x1b[1A\x1b[2K', end='')


def get_voltage(channel):
    adc = MCP3008(channel=channel)
    value = adc.value
    voltage = value * 3.3

    return voltage


def selector():
    color_value = 0

    while True:
        voltage = get_voltage(channel=0)
        color_value = int(voltage * (255 / 3.3))

        print(f"Calculated color value: {color_value}")
        clear_screen()
        channel = GPIO.wait_for_edge(
            21, GPIO.RISING, timeout=200, bouncetime=100)
        if channel is None:
            pass
        else:
            print("Color selected...")
            return color_value


def color_selector():
    color = [-1, -1, -1]

    for ch in range(3):
        color_value = selector()
        color[ch] = color_value

    return color


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


if __name__ == '__main__':
    setup()
    color = color_selector()
    
    print(f"Color: {color}")
