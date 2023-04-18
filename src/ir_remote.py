import RPi.GPIO as GPIO
import time

# Set the GPIO pin number for the IR receiver
IR_RECEIVER_GPIO = 14

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_RECEIVER_GPIO, GPIO.IN)

# Function to capture IR signals
def ir_callback(channel):
    # Get the received IR code
    code = GPIO.input(IR_RECEIVER_GPIO)
    if code == GPIO.LOW:
        # Print the received command to the console
        print("Received command: {}".format(code))

# Add event detection for IR signals
GPIO.add_event_detect(IR_RECEIVER_GPIO, GPIO.BOTH, callback=ir_callback)

# Main loop to keep the program running indefinitely
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        # Exit the program if Ctrl+C is pressed
        break

# Clean up GPIO
GPIO.remove_event_detect(IR_RECEIVER_GPIO)
GPIO.cleanup()