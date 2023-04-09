import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

# Set up PWM
pwm = GPIO.PWM(18, 100)
pwm.start(0)

# Define a function to play a tone on the buzzer
def play_tone(frequency, duration, volume=100):
    period = 1.0 / frequency
    delay = period / 2
    cycles = int(duration * frequency)

    # Set duty cycle based on volume (0-100)
    duty_cycle = volume / 100.0 * 100

    for i in range(cycles):
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(delay)
        pwm.ChangeDutyCycle(0)
        time.sleep(delay)
def play():
    t=0
    notes=[262,294,330,262,262,294,330,262,330,349,392,330,349,392,392,440,392,349,330,262,392,440,392,349,330,262,262,196,262,262,196,262]
    duration=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,1,0.25,0.25,0.25,0.25,0.5,0.5,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,1,0.5,0.5,1]
    for n in notes:
        play_tone(n, duration[t])
        time.sleep(duration[t] * 0.1)
        t+=1
        
try:
    # Play a series of tones
    play()
except KeyboardInterrupt:
    GPIO.cleanup()