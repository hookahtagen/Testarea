import RPi.GPIO as GPIO
import time

def detection(channel):
    global impulse_count
    impulse_count += 1
    print(impulse_count)


if __name__ == '__main__':
    global impulse_count
    
    GPIO.setmode(GPIO.BCM)

    detektor_pin = 26
    impulse_count = 0
    
    DELAY = 15
    
    start_time = time.time()
    
    GPIO.setup(detektor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(detektor_pin, GPIO.FALLING, callback=detection)

    try:
        print("Starting measurement...")
        print("This might take up to 60 seconds to gather\nthe data from the Geiger-Müller Counter\n\n")
        while True:
            time.sleep(DELAY) # Warten Sie 60 Sekunden, um die cpm zu berechnen
            elapsed_time = time.time() - start_time
            cpm = int(impulse_count / elapsed_time * DELAY)
            print("Counts per Minute: ", cpm)
            
            impulse_count = 0
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting...")
        
        GPIO.cleanup()