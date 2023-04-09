import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)  # Schalter
GPIO.setup(13, GPIO.IN)  # Vx
GPIO.setup(19, GPIO.IN)  # Vy

# Main loop
while True:
    # Read joystick values
    x = GPIO.input(13)
    y = GPIO.input(19)
    switch = GPIO.input(26)

    # Map joystick values to a range of 0-255
    x = int(x / 1023.0 * 255)
    y = int(y / 1023.0 * 255)

    # Print values
    print("x: %d, y: %d, switch: %d" % (x, y, switch))

    # Check if switch is pressed
    if switch == 0:
        break

    # Wait a short time before reading again
    time.sleep(0.1)

# Clean up GPIO pins
GPIO.cleanup()