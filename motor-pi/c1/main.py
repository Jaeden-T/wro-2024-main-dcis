import requests
import time
import gpiozero as gpio
from classes.dataStore import DataStoreObject
from classes.car import car
import numpy as npDeezNuts
import math as meth
import logging

logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M"
)


#! Varrible Decalarions that will change bellow:

#* Decaluartion
# Motor = Motor, need set enable
# Servo= angular serv
servo= gpio.AngularServo(27, min_angle=0, max_angle=90, initial_angle=45)

#* carSpeeds
CARSPEED = 1


#* Turn Prep
turnPrepDistance = 0
#* Data Get Frequiency
FREQUENCY = 1

#TODO Add API ENd Point to other pi 

#* Note to organsiers/markers: The pi is not over wifi but over withenet patch cables 



# 10 CM  before turn
WALLFWD = 10

#! End of varribles that may possibly change

#* Following car direction
#* wallMode[0] = The starting position

def calcWallType(data: DataStoreObject, theCar: car):
    if meth.close(data.ult_E + data.ult_W + theCar.length, 100, abs_tol=0.4):
        return 0
    
    if -meth.close(data.ult_E +data.ult_W + theCar.length, 60, abs_tol=0.4):
        return 1
    

def challenge1Movement():
    print("C1 LOADED")
    mapped = False

    calibrate = requests.get("http://pi3Sense.local:8000/calibrate")
    print(calibrate)
    motor = gpio.Motor(forward=23, backward=24, enable=25)
    
    # wallMode[1] = The place infront etc
    wallMode = [0,0,0,0]
    # If all the walfreqls are counted
    wallModeReady= False
    # Count the rounds
    roundsDone = 0
    
    # Storing Car Data
    dataStoreObjectArray = [] 
    theCar = car()
    
    # Segement 0 is the oriign
    currentSegement = 0
    data = requests.get("http://pi3Sense.local:8000/ult").json()

    while True:
        print("C1 TRUTH LOOP")
        try:
            data = requests.get("http://pi3Sense.local:8000/ult").json()
            imu = requests.get("http://pi3Sense.local:8000/imuData").json()
            dataStoreObjectArray.append(DataStoreObject(data["ult_N"]*100, data["ult_S"]*100, data["ult_E"]*100, data["ult_W"]*100, imu["z_rotation"]))
        except requests.exceptions.RequestException as e:
            logging.error(e)
        
        
        # if mapped == True:
        #     if calcWallType(dataStoreObjectArray[-1], theCar) == 1:
        #         wallMode[currentSegement] == 1
            
        #     elif calcWallType(dataStoreObjectArray[-1], theCar) == 0:
        #         wallMode[currentSegement] == 0
        #     else:
        #         wallMode[currentSegement] = 3
        
        
        # #! If mapping false
        # if mapped == False:
            
            #* Imu Check to see if dataStoreObjecctArray[-1].imu is close to 0, 90, 180, 360n values, check it the diffrence is within 5d, if it is then return false
            
            
            #* Assuming thats its in the straights 
            #TODO Add a constant for abs_ tol of turning to prevent false flagging
        
        if meth.isclose(dataStoreObjectArray[-1].imu, 0 )or  meth.isclose(dataStoreObjectArray[-1].imu, 90) or meth.isclose(dataStoreObjectArray[-1].imu, 180) or meth.isclose(dataStoreObjectArray[-1].imu, 360):
            logging.info("In a straight, continue as normal")

            
            #* If its in the straights keep moving FWD
            if dataStoreObjectArray[-1].ult_N > WALLFWD:
                if meth.isclose(dataStoreObjectArray[-1].ult_E, dataStoreObjectArray[-1].ult_W, abs_tol=2): #* If W and E are close, keeping moving fwd
                    servo.angle - 45
                    motor.forward(CARSPEED)
                    

                else: #* Else Turn in the direction thats needed
                    if dataStoreObjectArray[-1].ult_E > dataStoreObjectArray[-1].ult_W:
                        servo.angle = 60
                    else:
                        servo.angle = 30
            else:
                print("Servo Angle Set")
                servo.angle = 75
        
        
        # #* When not in the straights, eg major turn 
        # else:
        #     print("Is prolly turning")
        #     #* Wait till its close to the value
        #     motor.forward(CARSPEED)
        #     time.sleep(3)
        #     if not (meth.isclose(dataStoreObjectArray[-1].imu, 0 )or  meth.isclose(dataStoreObjectArray[-1].imu, 90) or meth.isclose(dataStoreObjectArray[-1].imu, 180) or meth.isclose(dataStoreObjectArray[-1].imu, 360)):
        #         motor.forward(CARSPEED)
                
        #     #* Once it exits the loop stop turning and reutrn to straight
        #     servo.angle = 45
        
        if meth.isclose(dataStoreObjectArray[-1].imu, 360):
            logging.debug("1 lap done ")
            roundsDone += 1
            
    # if mapped == True:
    #     while dataStoreObjectArray[-1].ult_N > WALLFWD:
    #         theCar.forward(CARSPEED)
        
            
            
    #         #* Maintain Straight Line
    #         if meth.abs(dataStoreObjectArray[-1].ult_E - dataStoreObjectArray[-1].ult_W) > 1:
    #             print("Execute further turning checks")
    #             logging.info("Execute further turning checks")
                
                
            
    #             #* CLear old data, export to file
    #         if len(dataStoreObjectArray) > 30:
    #             try:
    #                 with open("data.csv") as file:
    #                     file.append(dataStoreObjectArray[0].exportData())
    #                     #* Clear array histroical data
                
    #                     dataStoreObjectArray[0].pop(0)
                    
    #                 file.close()
    #             except:
    #                 print("Error here please, and a beep for error codes")
            
            
            
    #     if dataStoreObjectArray[-1].ult_N < WALLFWD:
    #         logging.info("Wall Turn Active")
    #         if wallModeReady == False:
    #             if ROTATIONDIRECTION == 2:
    #                 print("Right turn - clockwise")
    #                 #* tURN RIGHT IN ALL DIRECTIONS
                    
    #             elif ROTATIONDIRECTION == 3:
    #                 print("Let turn")
    #                 #* Turn Left (Anti clockwise)
                    
    #                 #* Calculate the optimal curve length given
            
    #         else:
    #             print("Alt turn mode")
    #             #* Alternative turn system with unkown wall lengths 
    #         #* While distance is more then
        
        

                
            
            time.sleep(FREQUENCY)


    
def predictRoute(wallSegements, whichSegement, position):
    print("Yea this one aint runnning")
    


