#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import math
import subprocess
import sys
import time
from rpi_ws281x import PixelStrip, Color
import argparse

from hc_sr04 import clear_screen

# LED strip configuration:
LED_COUNT = 16        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def heartbeat(strip, temperature, beat_freq=None):
    """Pulsate the LEDs like a heartbeat, smoothly changing colors from warm to cold
    based on the input temperature.

    Args:
        strip (neopixel.NeoPixel): NeoPixel strip object.
        temperature (float): Input temperature in Celsius.
        beat_freq (float): Frequency of the pulse waveform in hertz.

    """

    if beat_freq == None:
        beat_freq = 1.08
    else:
        beat_freq = beat_freq / 60.0

    color_lst = [
        (0, 0, 128),
        (135, 206, 235),
        (255, 255, 0),
        (255, 165, 0),
        (255, 69, 0),
        (128, 5, 2.5),
        (255, 0, 0)
    ]
    
    # Determine the color based on the input temperature.
    if temperature <= 0:
        print("pretty cold...")
        color = color_lst[0]  # dark blue
    elif 0 < temperature <= 10:
        color = color_lst[1]  # light blue
    elif 10 < temperature <= 15:
        color = color_lst[2]  # yellow
    elif 15 < temperature <= 20:
        color = color_lst[3]  # light orange
    elif 20 < temperature <= 25:
        color = color_lst[4]  # orange
    elif 25 < temperature <= 30:
        color = color_lst[5]  # light red
    else:
        print("poooh... it's hot")
        color = color_lst[6] # red

    # Define the pulse waveform as a cosine function.
    def pulse_waveform(t): return (
        1 + math.cos(2 * math.pi * beat_freq * t)) / 2

    # Pulsate the LEDs using the determined color and pulse waveform.
    t = 0
    while True:
        
        
        for i in range(strip.numPixels()):
            pulse_val = pulse_waveform(t)
            pixel_color = Color(
                int(pulse_val * float(color[0])),
                int(pulse_val * float(color[1])),
                int(pulse_val * float(color[2]))
            )
            strip.setPixelColor(i, pixel_color)
        strip.show()
        # adjust the sleep time based on the number of pixels and beat frequency
        time.sleep(1 / strip.numPixels() / beat_freq)
        t += 1 / strip.numPixels() / beat_freq


def read_bme280():
    command = ['read_bme280', '--i2c-bus', '3']
    max_retries = 5
    for i in range(max_retries):
        try:
            output = subprocess.check_output(
                command, stderr=subprocess.STDOUT).decode('utf-8')
            temperature = float(output.split("\n")[2].split()[0])
            pressure = float(output.split("\n")[0].split()[0])
            humidity = float(output.split("\n")[1].split()[0])
            return temperature
        except subprocess.CalledProcessError:
            return None


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true',
                        help='clear the display on exit')
    parser.add_argument('-t', '--temperature', type=int,
                        default=50, help='the input temperature (0-100)')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                       LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    print(f"Temperature: {args.temperature}")

    try:
        while True:
            heartbeat(strip, args.temperature, 125)
    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)


# if __name__ == '__main__':
#     # Process arguments
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-c', '--clear', action='store_true',
#                         help='clear the display on exit')
#     args = parser.parse_args()

#     # Create NeoPixel object with appropriate configuration.
#     strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ,
#                        LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
#     # Intialize the library (must be called once before other functions).
#     strip.begin()

#     print('Press Ctrl-C to quit.')
#     if not args.clear:
#         print('Use "-c" argument to clear LEDs on exit')

#     try:

#         while True:
#             print('Color wipe animations.')
#             colorWipe(strip, Color(255, 0, 0))  # Red wipe
#             colorWipe(strip, Color(0, 255, 0))  # Green wipe
#             colorWipe(strip, Color(0, 0, 255))  # Blue wipe
#             print('Theater chase animations.')
#             theaterChase(strip, Color(127, 127, 127))  # White theater chase
#             theaterChase(strip, Color(127, 0, 0))  # Red theater chase
#             theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
#             print('Rainbow animations.')
#             rainbow(strip)
#             rainbowCycle(strip)
#             theaterChaseRainbow(strip)

#     except KeyboardInterrupt:
#         if args.clear:
#             colorWipe(strip, Color(0, 0, 0), 10)
