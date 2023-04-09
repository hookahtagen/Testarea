import time
import smbus2
import bme280_2

port = 1
address = 0x76
bus = smbus2.SMBus(port)
time.sleep(1)
#calibration_params = bme280.load_calibration_params(bus, address)

data = bme280_2.sample(bus, address)

print(data.id)
print(data.timestamp)
print(data.temperature)
print(data.pressure)
print(data.humidity)


print(data)