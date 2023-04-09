from re import A
from unicodedata import name
import RPi.GPIO as GPIO
import time
GPIO.setmode( GPIO.BCM )

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
    A=18
    B=23
    C=24
    D=25
    
    motor = StepperMotor("motor1", [A,B,C,D], 0.002)
    
    degree = 180
    
    start = time.time()
    motor.turn_by_degree(True, degree)
    motor.turn_by_degree(False, degree)
    end = time.time()
    
    print(f"Time taken: {end-start} seconds")
    
    motor.cleanup()