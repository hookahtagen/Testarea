import RPi.GPIO as GPIO

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin 10 as input
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

i = 0


# Define a function to be called when an event is detected
def event_callback(channel):
    global i
    print(f"Event {i+1} detected on channel {channel}")
    i += 1


# Add event detection for rising and falling edges on GPIO pin 10
GPIO.add_event_detect(10, GPIO.RISING, callback=event_callback, bouncetime = 100)

# Wait for events
while True:
    try:
        pass
    except KeyboardInterrupt:
        break

# Clean up GPIO
GPIO.cleanup()
