import sys
import RPi.GPIO as GPIO
import time

from hc_sr04 import clear_screen

BUZZER = 18
notes = {
    "B0": 31,
    "C1": 33,
    "CS1": 35,
    "D1": 37,
    "DS1": 39,
    "E1": 41,
    "F1": 44,
    "FS1": 46,
    "G1": 49,
    "GS1": 52,
    "A1": 55,
    "AS1": 58,
    "B1": 62,
    "C2": 65,
    "CS2": 69,
    "D2": 73,
    "DS2": 78,
    "E2": 82,
    "F2": 87,
    "FS2": 93,
    "G2": 98,
    "GS2": 104,
    "A2": 110,
    "AS2": 117,
    "B2": 123,
    "C3": 131,
    "CS3": 139,
    "D3": 147,
    "DS3": 156,
    "E3": 165,
    "F3": 175,
    "FS3": 185,
    "G3": 196,
    "GS3": 208,
    "A3": 220,
    "AS3": 233,
    "B3": 247,
    "C4": 262,
    "CS4": 277,
    "D4": 294,
    "DS4": 311,
    "E4": 330,
    "F4": 349,
    "FS4": 370,
    "G4": 392,
    "GS4": 415,
    "A4": 440,
    "AS4": 466,
    "B4": 494,
    "C5": 523,
    "CS5": 554,
    "D5": 587,
    "DS5": 622,
    "E5": 659,
    "F5": 698,
    "FS5": 740,
    "G5": 784,
    "GS5": 831,
    "A5": 880,
    "AS5": 932,
    "B5": 988,
    "C6": 1047,
    "CS6": 1109,
    "D6": 1175,
    "DS6": 1245,
    "E6": 1319,
    "F6": 1397,
    "FS6": 1480,
    "G6": 1568,
    "GS6": 1661,
    "A6": 1760,
    "AS6": 1865,
    "B6": 1976,
    "C7": 2093,
    "CS7": 2217,
    "D7": 2349,
    "DS7": 2489,
    "E7": 2637,
    "F7": 2794,
    "FS7": 2960,
    "G7": 3136,
    "GS7": 3322,
    "A7": 3520,
    "AS7": 3729,
    "B7": 3951,
    "C8": 4186,
    "CS8": 4435,
    "D8": 4699,
    "DS8": 4978,
}
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)


def stop_at_button(channel):
    clear_screen()
    print("STOP sequence!\nExiting now...")
    GPIO.cleanup()
    sys.exit(0)


def set_emergency_stop(pin: int, FLAG: bool):
    interrupt_channel = pin
    GPIO.setup(interrupt_channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(interrupt_channel, GPIO.RISING if FLAG else GPIO.FALLING,
                          callback=stop_at_button, bouncetime=100)


def buzz(noteFreq, duration):
    halveWaveTime = 1 / (noteFreq * 2)
    waves = int(duration * noteFreq)
    for i in range(waves):
        GPIO.output(BUZZER, True)
        time.sleep(halveWaveTime)
        GPIO.output(BUZZER, False)
        time.sleep(halveWaveTime)


def play1():
    t = 0
    notes = [262, 294, 330, 262, 262, 294, 330, 262, 330, 349, 392, 330, 349, 392, 392,
             440, 392, 349, 330, 262, 392, 440, 392, 349, 330, 262, 262, 196, 262, 262, 196, 262]
    duration = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.25,
                0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 1]
    for n in notes:
        buzz(n, duration[t])
        time.sleep(duration[t] * 0.1)
        t += 1

def play2():
    global notes
    
    for note in notes.values():
        duration=0.25
        buzz(note, duration)
        
def beep_n_times(n: int) -> None:
    if n > 0:
        for _ in range(n):
            buzz(262, 0.1)
            time.sleep(0.15)


if __name__ == '__main__':
    set_emergency_stop(21)


    beep_n_times(8)
