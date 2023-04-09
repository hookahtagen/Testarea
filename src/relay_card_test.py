import RPi.GPIO as GPIO
import time

interval = 0.75


GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

flag = False
try:
    while True:
        GPIO.output(21, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(21, GPIO.LOW)
        time.sleep(interval / 2)

except KeyboardInterrupt:
    GPIO.cleanup()