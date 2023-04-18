import os
import sys
import time
import math
import RPi._GPIO as GPIO

from threading import Thread
from rpi_ws281x import PixelStrip, Color
from gpiozero import MCP3008

# from tm1637_base import TM1637


def clear_screen():
    # os.system("clear")
    print('\x1b[1A\x1b[2K', end='')
    

class constants:
    NUM_PIXELS=8 # 46
    DATA_OUT_PIN=18
    
    ADC_CHANNELS=8

class LedStrip:
    def __init__(self, name: str = "LedStrip", led_count: int = 8, data_out_pin: int = 18) -> None:
        self.name = name
        self.ref_voltage = 3.3

        self.led_count = led_count
        self.data_out_pin = data_out_pin

        self.brightness = 128
        self.color: tuple

        self.led_freq_hz = 800000
        self.led_dma = 10

        self.led_invert = False
        self.led_channel = 0

        self.strip = PixelStrip(self.led_count, self.data_out_pin, self.led_freq_hz,
                                self.led_dma, self.led_invert, self.brightness, self.led_channel)

        self.strip.begin()

        self.brightness_selector = Thread(
            target=self.strip_settings)

        self.is_running = False

        self.debounce = 100
        self.last_button_hit = 0.0

    def join(self):
        self.brightness_selector.join()

    def start(self):
        self.is_running = True
        self.brightness_selector.start()

    def stop(self):
        self.is_running = False

    def strip_settings(self):
        def format_color(rgb_values: list):
            rgb_values = [int(item * (255/3.3)) for item in rgb_values]
            return Color(rgb_values[0], rgb_values[1], rgb_values[2]), rgb_values

        start_time = time.time()
        while self.is_running:
            voltages = self.get_all_voltages() if self.is_running else None
            self.brightness = int(voltages[0] * (255/3.3))
            self.color, rgb_values = format_color(voltages[1:4])

            print(f"Brightness:\t{self.brightness}\tColor:\t{rgb_values}")

            self.strip.setBrightness(self.brightness)
            self.uni_color(self.color)

            time.sleep(.1)
            clear_screen()
            
        print("STOPPED")

    def get_all_voltages(self):
        voltages = []
        for channel in range(constants.ADC_CHANNELS):
            time.sleep(.001)
            adc = MCP3008(channel=channel)
            value = adc.value
            voltage = value * self.ref_voltage
            voltages.append(voltage)
            adc.close()

        return voltages

    @staticmethod
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

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, constants.NUM_PIXELS, 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, constants.NUM_PIXELS, 3):
                    self.strip.setPixelColor(i + q, 0)
    
    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(constants.NUM_PIXELS):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
    
    def heartbeat(self, temperature, beat_freq=None):
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
            
            
            for i in range(constants.NUM_PIXELS):
                pulse_val = pulse_waveform(t)
                pixel_color = Color(
                    int(pulse_val * float(color[0])),
                    int(pulse_val * float(color[1])),
                    int(pulse_val * float(color[2]))
                )
                self.strip.setPixelColor(i, pixel_color)
            self.strip.show()
            # adjust the sleep time based on the number of pixels and beat frequency
            time.sleep(1 / constants.NUM_PIXELS / beat_freq)
            t += 1 / constants.NUM_PIXELS / beat_freq

    def uni_color(self, rgb_color):
        # print("Unicolor")
        for i in range(0, constants.NUM_PIXELS, 1):
            self.strip.setPixelColor(i, rgb_color)
        self.strip.show()


def stop_at_button(channel):
    global led_strip
    led_strip.strip.setBrightness(0)
    led_strip.stop()
    
    for ch in range(constants.NUM_PIXELS):
        color = (0, 0, 0)  # Tuple representing RGB values
        color_value = (color[0] << 16) | (color[1] << 8) | color[2]  # Convert RGB values to 24-bit color value

        # Call the setPixelColor method with the 24-bit color value
        led_strip.strip.setPixelColor(ch, color_value)
    led_strip.strip.show()
    
    clear_screen()
    time.sleep(.5)
    print("STOP sequence!")
    print("Cleaning up")

    GPIO.cleanup()
    exit(0)


def set_emergency_stop(pin: int, FLAG: bool):
    interrupt_channel = pin
    GPIO.add_event_detect(interrupt_channel, GPIO.RISING if FLAG else GPIO.FALLING,
                          callback=stop_at_button, bouncetime=100)


def setup():
    led_strip = LedStrip("Strip", led_count=constants.NUM_PIXELS, data_out_pin=constants.DATA_OUT_PIN)
    led_strip.start()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    set_emergency_stop(21, True)

    return led_strip


if __name__ == '__main__':    
    flag = True
    if flag:
        rgb_color = (0, 0, 0)

        led_strip = setup()

        while led_strip.is_running:
            time.sleep(.5)
            
            if GPIO.input(21) == GPIO.HIGH and GPIO.input(26) == GPIO.HIGH:
                stop_at_button(-1)
                time.sleep(.1)
        
        while True:
            led_strip.rainbow(wait_ms=100)
            
            if GPIO.input(21) == GPIO.HIGH and GPIO.input(26) == GPIO.HIGH:
                stop_at_button(-1)
                time.sleep(.1)