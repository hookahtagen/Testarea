from time import sleep
from gpiozero import MCP3008

from hc_sr04 import clear_screen


def get_voltage():
    adc = MCP3008(channel=0)
    value = adc.value
    voltage = value * 3.3
    
    return voltage


if __name__ == '__main__':
    debug = False
    if debug == True:
        while True:
            clear_screen()
            voltage = get_voltage()
            print("Spannung: {}V".format(voltage))
            sleep(0.2)
    
    if debug == False:
        voltage = get_voltage()
        print(f"{voltage}")