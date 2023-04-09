import smbus2
import bme280

from hc_sr04 import clear_screen

if __name__ == '__main__':
    port: int = int(input("Enter a bus number: "))
    print("\n\n")
    
    address = 0x76
    bus = smbus2.SMBus(port)

    calibration_params = bme280.load_calibration_params(bus, address)

    # the sample method will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)

    clear_screen()
    # the compensated_reading class has the following attributes
    print(data.id)
    print(data.timestamp)
    print(data.temperature)
    print(data.pressure)
    print(data.humidity)

    # there is a handy string representation too
    print(data)