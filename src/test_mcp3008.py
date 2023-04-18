import os
from time import sleep
from gpiozero import MCP3008
import neopixel

def get_all_voltages():
        voltages = []
        for channel in range(8):
            sleep(.001)
            adc = MCP3008(channel=channel)
            value = adc.value
            voltage = value * 3.3
            voltages.append(voltage)
            adc.close()

        print("TEST")
        return voltages

def clear_screen():
    os.system("clear")

if __name__ == '__main__':
    debug = True
    if debug == True:
        try:
            while True:
                clear_screen()  
                voltages = get_all_voltages()
                for voltage in voltages[5:]:
                    print(f"Voltage: {voltage:.2f} V")
                sleep(.25)
        except Exception as e:
            print(e)
    
    if debug == False:
        voltage = get_all_voltages()
        print(f"{voltage}")