import RPi.GPIO as GPIO
import time

# Buzzer-Pin-Nummer
BUZZER_PIN = 19

# Frequenz für den Geigerzähler-Ton
GEIGER_FREQUENCY = 1000

def geiger_sound(duration):
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    
    # Play sound
    for i in range(duration):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(0.1)
    
    # Clean up GPIO
    GPIO.cleanup()
    

if __name__ == '__main__':
    geiger_sound(GEIGER_FREQUENCY)