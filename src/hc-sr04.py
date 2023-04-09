import math
from tkinter.messagebox import NO
import RPi.GPIO as GPIO
import time
import subprocess
GPIO.setmode(GPIO.BCM) 

class DistanceSensor:
    def __init__(self, trigger_pin=17, echo_pin=4):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def compensate_temperatur(self) -> float:
        speed_of_sound = 0
        command="bmp280"
        
        data = subprocess.check_output(command.split())
        data = data.decode("utf-8").split("\n")
        
        temperature, _, _ = data[0].split(" ")
        temperature = float(temperature)
        
        speed_of_sound = 331.3 * math.sqrt(1 + (temperature / 273.15)) 
        return speed_of_sound
        

    def measure_distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        start_time = time.time()
        end_time = time.time()

        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()

        while GPIO.input(self.echo_pin) == 1:
            end_time = time.time()

        speed_of_sound = self.compensate_temperatur()  # Compensate the effect of temperature on the speed of sound
        time_elapsed = end_time - start_time
        distance = (time_elapsed * speed_of_sound) / 2
        
        if distance < 2 or distance > 310:
            return -1
        
        return distance

    def measure_and_print_distance(self):
        try:
            while True:
                dist = self.measure_distance()
                if dist != -1:
                    print("Measured distance = %.1f cm" % dist)
                    time.sleep(1)
                else:
                    print("Out of range")
                    time.sleep(1)

        except KeyboardInterrupt:
            print("Measurement stopped by User")


class StepperMotor:
    def __init__(self, name: str, pinlist: list[int, int, int, int], speed: float) -> None:
        self.name = name
        self.pin = pinlist
        self.step_sleep = speed # 2ms    
        self.step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
        self.direction = False # True for clockwise, False for counter-clockwise
        self.step_sequence = [
            [1,0,0,1],
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1]]
        GPIO.setup( self.pin[0], GPIO.OUT )
        GPIO.setup( self.pin[1], GPIO.OUT )
        GPIO.setup( self.pin[2], GPIO.OUT )
        GPIO.setup( self.pin[3], GPIO.OUT )

        # initializing
        GPIO.output( self.pin[0], GPIO.LOW )
        GPIO.output( self.pin[1], GPIO.LOW )
        GPIO.output( self.pin[2], GPIO.LOW )
        GPIO.output( self.pin[3], GPIO.LOW )
        self.motor_pins = [self.pin[0],self.pin[1],self.pin[2],self.pin[3]]
        self.motor_step_counter = 0 ;
        
    def cleanup(self):
        GPIO.cleanup()
        
    def full_turn(self, mode: str):
        self.direction = mode
        try:
            self.motor_step_counter = 0
            i = 0
            for i in range(self.step_count):
                
                for pin in range(0, len(self.motor_pins)):
                    GPIO.output( self.motor_pins[pin], self.step_sequence[self.motor_step_counter][pin] )
                    
                if self.direction==True:
                    motor_step_counter = (motor_step_counter - 1) % 8
                    
                elif self.direction==False:
                    motor_step_counter = (motor_step_counter + 1) % 8
                    
                else: # defensive programming
                    print( "uh oh... direction should *always* be either True or False" )
                    self.cleanup()
                    
                time.sleep( self.step_sleep )

        except KeyboardInterrupt:
            pass
    
    def turn_by_degree(self, mode: str, degree: float) -> None:
        self.direction = mode
        one_degree: float = self.step_count / 360
        turn_rate: int = int(degree * one_degree)
        
        try:
            self.motor_step_counter = 0
            i = 0
            for i in range(turn_rate):
                
                for pin in range(0, len(self.motor_pins)):
                    GPIO.output( self.motor_pins[pin], self.step_sequence[self.motor_step_counter][pin] )
                    
                if self.direction==True:
                    self.motor_step_counter = (self.motor_step_counter - 1) % 8
                    
                elif self.direction==False:
                    self.motor_step_counter = (self.motor_step_counter + 1) % 8
                    
                else: # defensive programming
                    print( "uh oh... direction should *always* be either True or False" )
                    self.cleanup()
                    
                time.sleep( self.step_sleep )
        
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    pinlist = [18, 23, 24, 25]
    tracker = DistanceSensor()
    motor = StepperMotor(
        name="mot1",
        pinlist=pinlist,
        speed=0.002
    )
    try:
        while True:
            dist = tracker.measure_distance()
            print("Out of range") if dist == -1 else None
            if dist != -1:
                print(f"Measured distance = {dist:.1f} cm")
                if dist < 10:
                    motor.turn_by_degree(mode=True, degree=10)
                
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()