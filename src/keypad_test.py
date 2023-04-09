import RPi.GPIO as GPIO
import time

# Set up the GPIO pins for the rows and columns of the keypad
ROW_PINS = [14, 15, 18, 23]
COL_PINS = [24, 25, 8, 7]

# Define the key map


# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
for pin in ROW_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for pin in COL_PINS:
    GPIO.setup(pin, GPIO.OUT)

# Define a function to read the state of the keypad


def read_keypad():
    KEY_MAP = {
    (0, 0): '1',
    (0, 1): '2',
    (0, 2): '3',
    (0, 3): 'A',
    (1, 0): '4',
    (1, 1): '5',
    (1, 2): '6',
    (1, 3): 'B',
    (2, 0): '7',
    (2, 1): '8',
    (2, 2): '9',
    (2, 3): 'C',
    (3, 0): '*',
    (3, 1): '0',
    (3, 2): '#',
    (3, 3): 'D'}
    
    # Initialize the keys list to all None
    keys = [[None, None, None, None], [None, None, None, None],
            [None, None, None, None], [None, None, None, None]]
    # Loop through each row pin and column pin
    for row_num, row_pin in enumerate(ROW_PINS):
        for col_num, col_pin in enumerate(COL_PINS):
            # Set the current column pin to high
            GPIO.output(col_pin, GPIO.HIGH)
            # Read the state of the current row pin
            if GPIO.input(row_pin):
                # Update the keys list with the pressed key label
                keys[row_num][col_num] = KEY_MAP[(row_num, col_num)]
            # Set the current column pin back to low
            GPIO.output(col_pin, GPIO.LOW)
    # Return the keys list
    return keys


def read_motor_speed():
    speed = ''
    flag = False
    # Read the motor speed from the keypad - exit when the user hits the * key
    while not flag:
        # Read the state of the keypad
        keys = read_keypad()
        # Loop through each row in the keys list
        for row_num, row in enumerate(keys):
            # Loop through each key in the current row
            for col_num, key in enumerate(row):
                # Check if the current key has been pressed
                if key is not None:
                    # Check if the current key is the * key
                    conditions = [
                        '*',
                        'A',
                        'B',
                        'C',
                        'D'
                    ]
                    if key in conditions:
                        # Exit the loop
                        # Check if the key is a letter or a asterisk
                        if key in conditions[1:]:
                            # Set the speed to the corresponding value
                            speed = {
                                'A': '0.002',
                                'B': '0.004',
                                'C': '0.006',
                                'D': '0.008'
                            }[key]
                        if key == '*':
                            # Set the speed
                            # If a # is present in the speed string, replace it with a .
                            speed = float(speed.replace('#', '.'))                            

                        flag = True
                        return speed
                    # Otherwise, add the key to the speed string

                    speed += key
        # Wait 100ms before re-reading the keypad
        time.sleep(0.15)


# Loop indefinitely, reading the state of the keypad every 100ms
print("Please specify the motor speed (0.002 - 0.01).")
print("Or use one of the presets on buttons A - D")
print("Use the # key as a decimal point.")
print("Press * to set the speed.")

speed = read_motor_speed()
print(f"Motor speed set to {speed}")

# Clean up the GPIO pins
GPIO.cleanup()
