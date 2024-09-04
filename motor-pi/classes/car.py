from gpiozero import Servo
from RpiMotorLib import rpi_dc_lib

class car():
    def __init__(self):
        self.currentX = 0
        self.currentY = 0
        
        self.servo = Servo() #! SET THIS VALUE (SETVALUE)
        #*  (GPIO , GPIO , GPIO , freq , verbose, name) 
        self.motor = rpi_dc_lib.L298NMDc(1 ,True, "motor_one") #! (SETVALUE)

    def forward(self, cycle):
        self.motor.forward(cycle)
    def backwards(self, cycle):
        self.motor.backwards(cycle)
        
    def stop(self):
        self.motor.brake(0)
    