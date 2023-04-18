import time
import RPi.GPIO as GPIO
from gpiozero import MCP3008


from test_brightness import set_emergency_stop

def get_all_voltages():
    adc = MCP3008()
    voltages = []
    for channel in range(8):
        adc = MCP3008(channel=channel, differential=True)
        value = adc.value
        voltage = value * 3.3
        voltages.append(voltage)
        adc.close()
    return voltages

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    
    set_emergency_stop(21, True, None)
    
    
    while True:
        print('\x1b[1A\x1b[2K', end='')
        voltages = get_all_voltages()
        print(voltages)
        time.sleep(.5)