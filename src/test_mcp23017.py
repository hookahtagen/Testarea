import time
import smbus

# Define MCP23017 registers
MCP23017_IODIRA = 0x00   # I/O direction register A
MCP23017_GPIOA = 0x12    # GPIO port A register

# Define MCP23017 address and bus number
MCP23017_ADDR = 0x20     # Address of MCP23017
BUS_NUM = 1              # Bus number (usually 1 for Raspberry Pi 2+)

# Initialize I2C bus
bus = smbus.SMBus(BUS_NUM)

# Set I/O direction of MCP23017 (0xFF for input, 0x00 for output)
bus.write_byte_data(MCP23017_ADDR, MCP23017_IODIRA, 0xFF)

while True:
    # Read GPIOA register to get state of switch
    switch_state = bus.read_byte_data(MCP23017_ADDR, MCP23017_GPIOA) & 0x01
    if switch_state == 0:
        print("Switch is in OFF state")
    else:
        print("Switch is in ON state")
    time.sleep(.05)