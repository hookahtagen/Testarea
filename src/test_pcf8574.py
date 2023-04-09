import smbus2

# Festlegen der Adresse des PCF8574 auf dem i2c-Bus
DEVICE_ADDRESS = 0x20

# Öffnen einer Verbindung zum i2c-Bus 1
bus = smbus2.SMBus(1)

# Lesen der aktuellen Zustände aller 8 Eingänge des PCF8574
input_states = bus.read_byte(DEVICE_ADDRESS)

# Ausgabe der Zustände
print("Input states:", bin(input_states))
