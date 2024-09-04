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
    

def challenge1Movement(servo):
    global turnAngle
    turnAngle = 45
    
    print("C1 LOADED")
    mapped = False


    motor = gpio.Motor(forward=23, backward=24, enable=25)
    
    roundsDone = 0
    if roundsDone == 3:
        return 0
    # Count the rounds
    
    
    # Storing Car Data
    dataStoreObjectArray = [] 
    theCar = car()
    
    # Segement 0 is the oriign
    currentSegement = 0
    servo.angle = 45
    while True:
        if roundsDone == 3:
            motor.stop()
            return 0
        print("C1 TRUTH LOOP")
        try:
            data = requests.get("http://pi3Sense.local:8000/ult").json()
            imu = requests.get("http://pi3Sense.local:8000/imuData").json()
            print(imu)
            dataStoreObjectArray.append(DataStoreObject(data["ult_N"]*100, data["ult_S"]*100, data["ult_E"]*100, data["ult_W"]*100, imu["z_rotation"]))
            print(dataStoreObjectArray[-1].ult_N)
            print(dataStoreObjectArray[-1].ult_E)
            print(dataStoreObjectArray[-1].imu)
        except requests.exceptions.RequestException as e:
            logging.error(e)
        tolerance = 7
        
        imu = dataStoreObjectArray[-1].imu
        if(meth.isclose(imu, 0, abs_tol=tolerance) or 
            meth.isclose(imu, 90, abs_tol=tolerance) or 
            meth.isclose(imu, -90, abs_tol=tolerance) or 
            meth.isclose(imu, 180, abs_tol=tolerance) or 
            meth.isclose(imu, -180, abs_tol=tolerance) or
            meth.isclose(imu, 270, abs_tol=tolerance) or
            meth.isclose(imu, -270, abs_tol=tolerance) or
            meth.isclose(imu, 360, abs_tol=tolerance) or
            meth.isclose(imu, -360, abs_tol=tolerance)):
            #* Once it exits the loop stop turning and reutrn to straight
            servo.angle = 45
            print("In a straight, continue as normal")
            motor.forward(CARSPEED)
            if meth.isclose(dataStoreObjectArray[-1].imu, 360, abs_tol=5):
                print("1 lap done ")
                roundsDone += 1
            
            #* If its in the straights keep moving FWD
            if dataStoreObjectArray[-1].ult_N > WALLFWD:
                print("E and W")
                print(dataStoreObjectArray[-1].ult_E)
                print(dataStoreObjectArray[-1].ult_W)
                if meth.isclose(dataStoreObjectArray[-1].ult_E, dataStoreObjectArray[-1].ult_W, abs_tol=2): #* If W and E are close, keeping moving fwd
                    servo.angle - 45
                    
                    

                else: #* Else Turn in the direction thats needed 
                    servo.angle = 45
                    if dataStoreObjectArray[-1].ult_E > dataStoreObjectArray[-1].ult_W:
                        servo.angle = 60
                        turnAngle = 60
                    else:
                        servo.angle = 30
                        turnAngle = 30
                    
            else:
                
                if (dataStoreObjectArray[-1].ult_E - dataStoreObjectArray[-1].ult_W) > 10:
                
                    print("\n*5")
                    print("Servo Angle Set - > 10 ")
                    servo.angle = 20
                if (dataStoreObjectArray[-1].ult_W - dataStoreObjectArray[-1].ult_E) > 10:
                
                    print("\n*5")
                    print("Servo Angle Set W - E > 10")
                    servo.angle = 75
        
        #* When not in the straights, eg major turn 
        else:
            print("Is prolly turning")
            #* Wait till its close to the value
            servo.angle = turnAngle
            motor.forward(CARSPEED)
                

    

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
    


